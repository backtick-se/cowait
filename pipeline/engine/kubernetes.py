import os
import time
import kubernetes
from kubernetes import client, config, watch
from pipeline.tasks import TaskDefinition
from .const import ENV_TASK_CLUSTER
from .cluster import ClusterProvider, ClusterTask

DEFAULT_NAMESPACE = 'default'
DEFAULT_SUBDOMAIN = 'tasks'
LABEL_TASK_ID = 'pipeline/task'
LABEL_PARENT_ID = 'pipeline/parent'


class KubernetesTask(ClusterTask):
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
        self.hostname = f'{self.id}.{cluster.domain}'


class KubernetesProvider(ClusterProvider):
    def __init__(self, args={}):
        super().__init__('kubernetes', args)

        # hacky way to check if we're running within a pod
        if ENV_TASK_CLUSTER in os.environ:
            config.load_incluster_config()
        else:
            config.load_kube_config()

        configuration = client.Configuration()
        self.core = client.CoreV1Api(
            kubernetes.client.ApiClient(configuration))
        self.ext = client.ExtensionsV1beta1Api(
            kubernetes.client.ApiClient(configuration))
        self.custom = client.CustomObjectsApi(
            kubernetes.client.ApiClient(configuration))

    @property
    def namespace(self):
        return self.args.get('namespace', DEFAULT_NAMESPACE)

    @property
    def domain(self):
        return self.args.get('domain', 'cluster.backtick.se')

    @property
    def timeout(self):
        return self.args.get('timeout', 180)

    def spawn(self, taskdef: TaskDefinition) -> KubernetesTask:
        ports = []
        rules = []

        for path, port in taskdef.routes.items():
            ports.append(client.V1ServicePort(
                name='web',
                port=port,
                target_port=port,
            ))

            rules.append(client.ExtensionsV1beta1IngressRule(
                host=f'{taskdef.id}.{self.domain}',
                http=client.ExtensionsV1beta1HTTPIngressRuleValue(
                    paths=[
                        client.ExtensionsV1beta1HTTPIngressPath(
                            path=path,
                            backend=client.ExtensionsV1beta1IngressBackend(
                                service_name=taskdef.id,
                                service_port='web',
                            ),
                        ),
                    ],
                ),
            ))

            taskdef.routes[path] = {
                'port': port,
                'path': path,
                'url': f'https://{taskdef.id}.{self.domain}{path}',
            }

        # container definition
        container = client.V1Container(
            name=taskdef.id,
            image=taskdef.image,
            env=self.create_env(taskdef),
            ports=self.create_ports(taskdef),
            image_pull_policy='Always',  # taskdef field??
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

        if len(rules):
            print('~~ creating task ingress', path, '-> port', port)

            self.core.create_namespaced_service(
                namespace=self.namespace,
                body=client.V1Service(
                    metadata=client.V1ObjectMeta(
                        name=taskdef.id,
                        namespace=self.namespace,
                        labels={
                            LABEL_TASK_ID: taskdef.id,
                        },
                    ),
                    spec=client.V1ServiceSpec(
                        selector={
                            LABEL_TASK_ID: taskdef.id,
                        },
                        ports=ports,
                    ),
                ),
            )

            self.ext.create_namespaced_ingress(
                namespace=self.namespace,
                body=client.ExtensionsV1beta1Ingress(
                    metadata=client.V1ObjectMeta(
                        name=taskdef.id,
                        labels={
                            LABEL_TASK_ID: taskdef.id,
                        },
                        annotations={
                            'kubernetes.io/ingress.class': 'traefik',
                            'traefik.frontend.rule.type': 'PathPrefix',
                        },
                    ),
                    spec=client.ExtensionsV1beta1IngressSpec(
                        rules=rules,
                    ),
                ),
            )

        # wait for pod to become ready
        timeout = self.timeout
        while True:
            pod = self.get_task_pod(taskdef.id)
            if pod and pod.status.phase != 'Pending':
                break
            timeout -= 1
            if timeout == 0:
                raise TimeoutError(f'Could not find pod for {taskdef.id}')
            time.sleep(1)

        # wrap & return task
        print('~~ created kubenetes pod', pod.metadata.name)
        return KubernetesTask(self, taskdef, pod)

    def kill(self, task_id):
        self.core.delete_collection_namespaced_pod(
            namespace=self.namespace,
            label_selector=f'{LABEL_TASK_ID}={task_id}',
        )
        return task_id

    def get_task_pod(self, task_id):
        res = self.core.list_namespaced_pod(
            namespace=self.namespace,
            label_selector=f'{LABEL_TASK_ID}={task_id}',
        )
        return res.items[0] if len(res.items) > 0 else None

    def get_task_child_pods(self, task_id: str):
        res = self.core.list_namespaced_pod(
            namespace=self.namespace,
            label_selector=f'{LABEL_PARENT_ID}={task_id}',
        )
        return res.items

    def wait(self, task: KubernetesTask) -> None:
        raise NotImplementedError()

    def logs(self, task: KubernetesTask):
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
        raise NotImplementedError()

    def list_all(self) -> list:
        raise NotImplementedError()

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
