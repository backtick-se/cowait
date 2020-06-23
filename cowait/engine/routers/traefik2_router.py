from kubernetes import client
from .router import Router
from ..const import LABEL_TASK_ID


TRAEFIK2_API_GROUP = 'traefik.containo.us'
TRAEFIK2_API_VERSION = 'v1alpha1'
TRAEFIK2_API_NAMESPACE = 'default'
TRAEFIK2_INGRESSROUTE = 'IngressRoute'
TRAEFIK2_INGRESSROUTE_PLURAL = 'ingressroutes'


class Traefik2Router(Router):
    def __init__(self, cluster):
        super().__init__(cluster)
        cluster.on('prepare', self.on_prepare)
        cluster.on('spawn', self.on_spawn)
        cluster.on('kill', self.on_kill)

        self.config = cluster.args.get('traefik2', {})
        self.secure = self.config.get('secure', False)
        self.middlewares = self.config.get('middlewares', [])
        self.entrypoints = self.config.get('entrypoints', ['web'])

    def on_prepare(self, taskdef):
        domain = self.cluster.domain
        if domain is None:
            raise RuntimeError('No cluster domain configured')

        protocol = 'https' if self.secure else 'http'

        for path, port in taskdef.routes.items():
            if len(path) < 1 and path[0] != '/':
                raise RuntimeError(f'Paths must start with /, got {path}')

            taskdef.routes[path] = {
                'port': port,
                'path': path,
                'url': f'{protocol}://{taskdef.id}.{domain}{path}',
            }

        return taskdef

    def on_spawn(self, task):
        ports = []
        routes = []

        idx = 0
        for path, route in task.routes.items():
            port = route['port']
            idx += 1

            ports.append(client.V1ServicePort(
                port=port,
                target_port=port,
            ))

            host = f'{task.id}.{self.cluster.domain}'
            routes.append({
                'match': f'Host(`{host}`) && PathPrefix(`{path}`)',
                'middlewares': self.middlewares,
                'kind': 'Rule',
                'services': [
                    {'name': task.id, 'port': port}
                ]
            })

        if len(routes) == 0:
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

        self.cluster.custom.create_namespaced_custom_object(
            group=TRAEFIK2_API_GROUP,
            version=TRAEFIK2_API_VERSION,
            plural=TRAEFIK2_INGRESSROUTE_PLURAL,
            namespace=TRAEFIK2_API_NAMESPACE,
            body={
                'apiVersion': f'{TRAEFIK2_API_GROUP}/{TRAEFIK2_API_VERSION}',
                'kind': TRAEFIK2_INGRESSROUTE,
                'metadata': {
                    'name': f'{task.id}',
                    'namespace': self.cluster.namespace,
                    'labels': {
                        LABEL_TASK_ID: task.id,
                        'ingress-for': task.id
                    },
                },
                'spec': {
                    'entryPoints': self.entrypoints,
                    'routes': routes,
                }
            },
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
            self.cluster.custom.delete_cluster_custom_object(
                group=TRAEFIK2_API_GROUP,
                version=TRAEFIK2_API_VERSION,
                plural=TRAEFIK2_INGRESSROUTE_PLURAL,
                name=task_id,
            )
        except client.rest.ApiException:
            pass
