import os
import time
import kubernetes
import urllib3.exceptions
from kubernetes import client, config, watch
from cowait.tasks import TaskDefinition, RemoteTask
from .const import ENV_TASK_CLUSTER, LABEL_TASK_ID, LABEL_PARENT_ID
from .cluster import ClusterProvider
from .errors import TaskCreationError, ProviderError
from .routers import create_router

DEFAULT_NAMESPACE = 'default'


class KubernetesTask(RemoteTask):
    def __init__(
        self,
        cluster: ClusterProvider,
        taskdef: TaskDefinition,
        pod,
    ):
        super().__init__(
            cluster=cluster,
            taskdef=taskdef,
        )
        self.pod = pod
        self.ip = self.pod.status.pod_ip


class KubernetesProvider(ClusterProvider):
    def __init__(self, args={}):
        super().__init__('kubernetes', args)

        # hacky way to check if we're running within a pod
        if ENV_TASK_CLUSTER in os.environ:
            config.load_incluster_config()
        else:
            config.load_kube_config(context=self.args.get('context', None))

        configuration = client.Configuration()
        self.client = kubernetes.client.ApiClient(configuration)
        self.core = client.CoreV1Api(self.client)
        self.ext = client.ExtensionsV1beta1Api(self.client)
        self.custom = client.CustomObjectsApi(self.client)

        self.router = create_router(self, self.args.get('router', 'none'))

    @property
    def namespace(self):
        return self.args.get('namespace', DEFAULT_NAMESPACE)

    @property
    def domain(self):
        return self.args.get('domain', None)

    @property
    def timeout(self):
        return self.args.get('timeout', 180)

    def spawn(self, taskdef: TaskDefinition) -> KubernetesTask:
        try:
            self.emit_sync('prepare', taskdef=taskdef)

            # container definition
            container = client.V1Container(
                name=taskdef.id,
                image=taskdef.image,
                env=self.create_env(taskdef),
                ports=self.create_ports(taskdef),
                image_pull_policy='Always',  # taskdef field??
                resources=client.V1ResourceRequirements(
                    limits={
                        'cpu': str(taskdef.cpu),
                        'memory': str(taskdef.memory),
                    },
                    requests={
                        'cpu': str(taskdef.cpu),
                        'memory': str(taskdef.memory),
                    },
                ),
            )

            pod = self.core.create_namespaced_pod(
                namespace=self.namespace,
                body=client.V1Pod(
                    metadata=client.V1ObjectMeta(
                        name=taskdef.id,
                        namespace=self.namespace,
                        labels={
                            LABEL_TASK_ID: taskdef.id,
                            LABEL_PARENT_ID: taskdef.parent,
                            **taskdef.meta,
                        },
                    ),
                    spec=client.V1PodSpec(
                        hostname=taskdef.id,
                        restart_policy='Never',
                        image_pull_secrets=self.get_pull_secrets(),

                        containers=[container],
                    ),
                ),
            )

            # wrap & return task
            print('~~ created kubenetes pod', pod.metadata.name)
            task = KubernetesTask(self, taskdef, pod)
            self.emit_sync('spawn', task=task)
            return task

        except urllib3.exceptions.MaxRetryError:
            raise ProviderError('Kubernetes engine unavailable')

    def kill(self, task_id):
        try:
            self.core.delete_collection_namespaced_pod(
                namespace=self.namespace,
                label_selector=f'{LABEL_TASK_ID}={task_id}',
            )
            self.emit_sync('kill', task_id=task_id)
            return task_id

        except urllib3.exceptions.MaxRetryError:
            raise ProviderError('Kubernetes engine unavailable')

    def get_task_pod(self, task_id):
        try:
            res = self.core.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f'{LABEL_TASK_ID}={task_id}',
            )
            return res.items[0] if len(res.items) > 0 else None

        except urllib3.exceptions.MaxRetryError:
            raise ProviderError('Kubernetes engine unavailable')

    def get_task_child_pods(self, task_id: str):
        try:
            res = self.core.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f'{LABEL_PARENT_ID}={task_id}',
            )
            return res.items

        except urllib3.exceptions.MaxRetryError:
            raise ProviderError('Kubernetes engine unavailable')

    def wait(self, task: KubernetesTask) -> None:
        raise NotImplementedError()

    def wait_until_ready(self, task_id: str, poll_interval: float = 0.5):
        timeout = self.timeout
        while True:
            time.sleep(poll_interval)
            pod = self.get_task_pod(task_id)

            statuses = pod.status.container_statuses
            if statuses is not None and len(statuses) > 0:
                state = statuses[0].state

                # check for termination errors
                if state.terminated is not None:
                    raise TaskCreationError(
                        f'Pod terminated: {state.terminated.reason}\n'
                        f'{state.terminated.message}')

                # check waiting state
                if state.waiting is not None:
                    # abort if the image is not available
                    if state.waiting.reason == 'ErrImagePull':
                        self.kill(task_id)
                        raise TaskCreationError(
                            f'Image pull failed\n'
                            f'{state.waiting.message}')

                # we are go
                if state.running is not None:
                    break

            timeout -= poll_interval
            if timeout <= 0:
                raise TimeoutError(f'Could not find pod for {task_id}')

    def logs(self, task: KubernetesTask):
        # wait for pod to become ready
        self.wait_until_ready(task.id)

        try:
            w = watch.Watch()
            return w.stream(
                self.core.read_namespaced_pod_log,
                name=task.id,
                namespace=self.namespace,
            )
        except Exception:
            self.logs(task)

    def destroy_all(self) -> list:
        try:
            self.core.delete_collection_namespaced_pod(
                namespace=self.namespace,
                label_selector=LABEL_TASK_ID,
            )

        except urllib3.exceptions.MaxRetryError:
            raise ProviderError('Kubernetes engine unavailable')

    def list_all(self) -> list:
        try:
            res = self.core.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=LABEL_TASK_ID,
            )
            return map(lambda pod: pod.metadata.name, res.items)

        except urllib3.exceptions.MaxRetryError:
            raise ProviderError('Kubernetes engine unavailable')

    def destroy(self, task_id) -> list:
        def kill_family(task_id):
            print('~~ kubernetes kill', task_id)

            kills = []
            children = self.get_task_child_pods(task_id)
            for child in children:
                child_id = child.metadata.labels[LABEL_TASK_ID]
                kills += kill_family(child_id)

            self.kill(task_id)
            kills.append(task_id)
            return kills

        return kill_family(task_id)

    def destroy_children(self, parent_id: str) -> list:
        try:
            # get a list of child pods
            children = self.core.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f'{LABEL_PARENT_ID}={parent_id}',
            )

            # destroy child pods
            self.core.delete_collection_namespaced_pod(
                namespace=self.namespace,
                label_selector=f'{LABEL_PARENT_ID}={parent_id}',
            )

            # return killed child ids
            return [
                child.metadata.labels[LABEL_TASK_ID]
                for child in children.items
            ]

        except urllib3.exceptions.MaxRetryError:
            raise ProviderError('Kubernetes engine unavailable')

    def create_env(self, taskdef: TaskDefinition):
        env = super().create_env(taskdef)
        return [
            client.V1EnvVar(str(name), str(value))
            for name, value in env.items()
        ]

    def create_ports(self, taskdef: TaskDefinition) -> list:
        return [
            client.V1ContainerPort(**convert_port(port, host_port))
            for port, host_port in taskdef.ports.items()
        ]

    def get_pull_secrets(self):
        secrets = self.args.get('pull_secrets', ['docker'])
        return [client.V1LocalObjectReference(name=s) for s in secrets]

    def find_agent(self):
        pod = self.get_task_pod('agent')
        if pod is None:
            return None
        if pod.status.phase != 'Running':
            return None

        token = pod.metadata.labels['http_token']
        return f'ws://{pod.status.pod_ip}/ws?token={token}'


def convert_port(port, host_port: str = None):
    protocol = 'TCP'
    if isinstance(port, str) and '/' in port:
        slash = port.find('/')
        protocol = port[slash+1:]
        port = port[:slash]

    if host_port is None:
        host_port = port

    return {
        'protocol': protocol.upper(),
        'container_port': int(port),
        'host_port': int(host_port),
    }
