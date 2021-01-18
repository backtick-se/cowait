import time
import kubernetes
import urllib3.exceptions
from kubernetes import client, config, watch
from cowait.network import get_remote_url
from cowait.tasks import TaskDefinition
from cowait.utils import json_stream
from cowait.engine.const import LABEL_TASK_ID, LABEL_PARENT_ID
from cowait.engine.cluster import ClusterProvider
from cowait.engine.errors import ProviderError, TaskCreationError
from cowait.engine.routers import create_router
from .task import KubernetesTask
from .volumes import create_volumes
from .utils import create_ports
from .affinity import create_affinity

DEFAULT_NAMESPACE = 'default'
DEFAULT_SERVICE_ACCOUNT = 'default'


class KubernetesProvider(ClusterProvider):
    def __init__(self, args={}):
        super().__init__('kubernetes', args)

        try:
            # attempt to load incluster config if available
            config.load_incluster_config()
        except kubernetes.config.ConfigException:
            # load local config
            config.load_kube_config(context=self.args.get('context', None))

        self.client = kubernetes.client.ApiClient(client.Configuration().get_default_copy())
        self.core = client.CoreV1Api(self.client)
        self.ext = client.ExtensionsV1beta1Api(self.client)
        self.custom = client.CustomObjectsApi(self.client)

        self.router = create_router(self, self.args.get('router', 'none'))

    @property
    def namespace(self):
        return self.args.get('namespace', DEFAULT_NAMESPACE)

    @property
    def service_account(self):
        return self.args.get('service_account', DEFAULT_SERVICE_ACCOUNT)

    @property
    def domain(self):
        return self.args.get('domain', None)

    @property
    def timeout(self):
        return self.args.get('timeout', 180)

    def spawn(self, taskdef: TaskDefinition) -> KubernetesTask:
        try:
            self.emit_sync('prepare', taskdef=taskdef)

            volumes, mounts = create_volumes(taskdef.volumes)

            # container definition
            container = client.V1Container(
                name=taskdef.id,
                image=taskdef.image,
                env=self.create_env(taskdef),
                ports=create_ports(taskdef.ports),
                image_pull_policy='Always',  # taskdef field??
                resources=client.V1ResourceRequirements(
                    requests={
                        'cpu': str(taskdef.cpu or '0'),
                        'memory': str(taskdef.memory or '0'),
                    },
                    limits={
                        'cpu': str(taskdef.cpu_limit or '0'),
                        'memory': str(taskdef.memory_limit or '0'),
                    },
                ),
                volume_mounts=mounts,
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
                        volumes=volumes,

                        containers=[container],
                        service_account_name=self.service_account,
                        affinity=create_affinity(taskdef.affinity),
                    ),
                ),
            )

            # wrap & return task
            # print('~~ created kubenetes pod', pod.metadata.name)
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

    def wait(self, task: KubernetesTask) -> bool:
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
        if not isinstance(task, KubernetesTask):
            raise TypeError('Expected a valid KubernetesTask')

        # wait for pod to become ready
        self.wait_until_ready(task.id)

        try:
            w = watch.Watch()
            logs = w.stream(
                self.core.read_namespaced_pod_log,
                name=task.id,
                namespace=self.namespace,
            )

            def add_newline_stream(task):
                for log in logs:
                    yield log + '\n'

            return json_stream(add_newline_stream(task))

        except Exception:
            return self.logs(task)

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
            running = filter(lambda pod: pod.status.phase == 'Running', res.items)
            ids = map(lambda pod: pod.metadata.name, running)
            return ids

        except urllib3.exceptions.MaxRetryError as e:
            raise ProviderError('Kubernetes engine unavailable')

    def destroy(self, task_id) -> list:
        def kill_family(task_id):
            # print('~~ kubernetes kill', task_id)

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

    def get_pull_secrets(self):
        secrets = self.args.get('pull_secrets', [])
        return [client.V1LocalObjectReference(name=s) for s in secrets]

    def find_agent(self):
        pod = self.get_task_pod('agent')
        if pod is None:
            return None
        if pod.status.phase != 'Running':
            return None

        token = pod.metadata.labels['http_token']
        return get_remote_url(pod.status.pod_ip, token)
