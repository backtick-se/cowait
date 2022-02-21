from kubernetes import client
from .router import Router
from ..kubernetes import KubernetesProvider
from ..const import LABEL_TASK_ID


class TraefikRouter(Router):
    cluster: KubernetesProvider

    def __init__(self, cluster):
        super().__init__(cluster)
        if not isinstance(cluster, KubernetesProvider):
            raise TypeError('TraefikRouter can only be used with a Kubernetes provider')

        cluster.on('prepare', self.on_prepare)
        cluster.on('spawn', self.on_spawn)
        cluster.on('kill', self.on_kill)

    def on_prepare(self, taskdef):
        domain = self.cluster.domain
        if domain is None:
            raise RuntimeError('No cluster domain configured')

        for path, port in taskdef.routes.items():
            taskdef.routes[path] = {
                'port': port,
                'path': path,
                'url': f'http://{taskdef.id}.{domain}{path}',
            }
        return taskdef

    def on_spawn(self, task):
        ports = []
        rules = []

        idx = 0
        for path, route in task.routes.items():
            port = route['port']
            idx += 1
            port_name = f'route{idx}'

            ports.append(client.V1ServicePort(
                name=port_name,
                port=port,
                target_port=port,
            ))

            rules.append(client.V1IngressRule(
                host=f'{task.id}.{self.cluster.domain}',
                http=client.V1IngressRuleValue(
                    paths=[
                        client.V1IngressPath(
                            path=path,
                            backend=client.V1IngressBackend(
                                service_name=task.id,
                                service_port=port_name,
                            ),
                        ),
                    ],
                ),
            ))

        if len(rules) == 0:
            return

        print('~~ creating task ingress', path, '-> port', port)

        self.cluster.core.create_namespaced_service(
            namespace=self.cluster.namespace,
            body=client.V1Service(
                metadata=client.V1ObjectMeta(
                    name=task.id,
                    namespace=self.cluster.namespace,
                    labels={
                        LABEL_TASK_ID: task.id,
                    },
                ),
                spec=client.V1ServiceSpec(
                    selector={
                        LABEL_TASK_ID: task.id,
                    },
                    ports=ports,
                ),
            ),
        )

        self.cluster.networking.create_namespaced_ingress(
            namespace=self.cluster.namespace,
            body=client.V1Ingress(
                metadata=client.V1ObjectMeta(
                    name=task.id,
                    labels={
                        LABEL_TASK_ID: task.id,
                    },
                    annotations={
                        'kubernetes.io/ingress.class': 'traefik',
                        'traefik.frontend.rule.type': 'PathPrefix',
                    },
                ),
                spec=client.V1IngressSpec(
                    rules=rules,
                ),
            ),
        )

    def on_kill(self, task_id):
        try:
            self.cluster.core.delete_namespaced_service(
                namespace=self.cluster.namespace,
                name=task_id,
            )
        except client.rest.ApiException:
            pass

        try:
            self.cluster.networking.delete_namespaced_ingress(
                namespace=self.cluster.namespace,
                name=task_id
            )
        except client.rest.ApiException:
            pass
