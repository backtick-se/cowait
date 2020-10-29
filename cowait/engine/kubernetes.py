import time
import kubernetes
import urllib3.exceptions
from kubernetes import client, config, watch
from cowait.tasks import TaskDefinition, RemoteTask
from cowait.utils import json_stream
from .const import LABEL_TASK_ID, LABEL_PARENT_ID
from .cluster import ClusterProvider
from .errors import TaskCreationError, ProviderError
from .routers import create_router

DEFAULT_NAMESPACE = 'default'
DEFAULT_SERVICE_ACCOUNT = 'default'

VOLUME_SOURCES = {
    'aws_elastic_block_store': client.V1AWSElasticBlockStoreVolumeSource,
    'azure_disk': client.V1AzureDiskVolumeSource,
    'azure_file': client.V1AzureFileVolumeSource,
    'cephfs': client.V1CephFSVolumeSource,
    'cinder': client.V1CinderVolumeSource,
    'config_map': client.V1ConfigMapVolumeSource,
    'csi': client.V1CSIVolumeSource,
    'downward_api': client.V1DownwardAPIVolumeSource,
    'empty_dir': client.V1EmptyDirVolumeSource,
    'fc': client.V1FCVolumeSource,
    'flex_volume': client.V1FlexVolumeSource,
    'flocker': client.V1FlockerVolumeSource,
    'gce_persistent_disk': client.V1GCEPersistentDiskVolumeSource,
    'git_repo': client.V1GitRepoVolumeSource,
    'glusterfs': client.V1GlusterfsVolumeSource,
    'host_path': client.V1HostPathVolumeSource,
    'iscsi': client.V1ISCSIVolumeSource,
    'nfs': client.V1NFSVolumeSource,
    'persistent_volume_claim': client.V1PersistentVolumeClaimVolumeSource,
    'photon_persistent_disk': client.V1PhotonPersistentDiskVolumeSource,
    'portworx_volume': client.V1PortworxVolumeSource,
    'projected': client.V1ProjectedVolumeSource,
    'quobyte': client.V1QuobyteVolumeSource,
    'rbd': client.V1RBDVolumeSource,
    'scale_io': client.V1ScaleIOVolumeSource,
    'secret': client.V1SecretVolumeSource,
    'storageos': client.V1StorageOSVolumeSource,
    'vsphere_volume': client.V1VsphereVirtualDiskVolumeSource,
}


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

    def __str__(self):
        return f'KubernetesTask({self.id}, {self.status}, {self.inputs})'


class KubernetesProvider(ClusterProvider):
    def __init__(self, args={}):
        super().__init__('kubernetes', args)

        try:
            # attempt to load incluster config if available
            config.load_incluster_config()
        except kubernetes.config.ConfigException:
            # load local config
            config.load_kube_config(context=self.args.get('context', None))

        self.client = kubernetes.client.ApiClient(client.Configuration())
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
                ports=self.create_ports(taskdef),
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

        except urllib3.exceptions.MaxRetryError:
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


def create_volumes(task_volumes):
    index = 0
    mounts = []
    volumes = []
    for target, volume in task_volumes.items():
        index += 1
        name = volume.get('name', f'volume{index}')
        for source_type, VolumeSource in VOLUME_SOURCES.items():
            if source_type not in volume:
                continue

            volume_config = volume[source_type]
            volumes.append(client.V1Volume(**{
                'name': name,
                source_type: VolumeSource(**volume_config),
            }))
            mounts.append(client.V1VolumeMount(
                name=name,
                read_only=volume.get('read_only', False),
                mount_path=target,
            ))

    return volumes, mounts


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
