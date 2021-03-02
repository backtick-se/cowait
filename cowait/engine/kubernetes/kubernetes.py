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
from .utils import create_env, create_ports
from .affinity import create_affinity
from .pod import pod_is_ready, extract_pod_taskdef
from .errors import PodUnschedulableError, PodTerminatedError, ImagePullError

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

        self.core = client.CoreV1Api()
        self.ext = client.ExtensionsV1beta1Api()
        self.custom = client.CustomObjectsApi()

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
                env=create_env(self, taskdef),
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

    def wait_until_ready(self, task_id: str, poll_interval: float = 1):
        while True:
            time.sleep(poll_interval)
            pod = self.get_task_pod(task_id)
            if not pod:
                raise ProviderError(f'No such task: {task_id}')

            try:
                if pod_is_ready(pod):
                    break
                else:
                    poll_interval = 1

            except PodUnschedulableError as e:
                poll_interval = 10
                print('warning: task', task_id, 'is unschedulable:', str(e))

            except PodTerminatedError:
                raise TaskCreationError('Task terminated') from None
            
            except ImagePullError:
                self.kill(task_id)
                raise TaskCreationError('Image pull failed') from None

    def logs(self, task_id: str):
        # wait for pod to become ready
        self.wait_until_ready(task_id)

        try:
            w = watch.Watch()
            logs = w.stream(
                self.core.read_namespaced_pod_log,
                name=task_id,
                namespace=self.namespace,
            )

            def add_newline_stream():
                for log in logs:
                    yield log + '\n'

            return json_stream(add_newline_stream())

        except Exception:
            return self.logs(task_id)

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
            return [
                KubernetesTask(self, extract_pod_taskdef(pod), pod)
                for pod in running
            ]

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

