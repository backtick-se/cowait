from typing import List
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

    @property
    def secure(self) -> bool:
        return self.cert_resolver is not None

    @property
    def middlewares(self) -> List[str]:
        return self.config.get('middlewares', [])

    @property
    def entrypoints(self) -> List[str]:
        return self.config.get('entrypoints', ['web', 'websecure'])

    @property
    def cert_resolver(self) -> str:
        return self.config.get('certresolver', None)

    @property
    def domain(self) -> str:
        domain = self.cluster.domain
        if domain is None:
            raise RuntimeError('No cluster domain configured')
        return domain

    def on_prepare(self, taskdef):
        protocol = 'https' if self.secure else 'http'

        for path, port in taskdef.routes.items():
            if len(path) < 1 and path[0] != '/':
                raise RuntimeError(f'Paths must start with /, got {path}')

            taskdef.routes[path] = {
                'port': int(port),
                'path': path,
                'url': f'{protocol}://{taskdef.id}.{self.domain}{path}',
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
                port=int(port),
                target_port=int(port),
            ))

            host = f'{task.id}.{self.cluster.domain}'
            routes.append({
                'kind': 'Rule',
                'match': f'Host(`{host}`) && PathPrefix(`{path}`)',
                'middlewares': self.middlewares,
                'services': [
                    {'name': task.id, 'port': int(port)}
                ],
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

        ingress = {
            'entryPoints': self.entrypoints,
            'routes': routes,
        }
        if self.secure:
            ingress['tls'] = {
                'certResolver': self.cert_resolver,
            }

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
                'spec': ingress,
            },
        )

    def on_kill(self, task_id):
        try:
            self.cluster.core.delete_namespaced_service(
                namespace=self.cluster.namespace,
                name=task_id,
            )
        except client.rest.ApiException as e:
            if e.status != 404:
                print('!! error deleting Kubernetes Service:', e)

        try:
            self.cluster.custom.delete_namespaced_custom_object(
                group=TRAEFIK2_API_GROUP,
                version=TRAEFIK2_API_VERSION,
                plural=TRAEFIK2_INGRESSROUTE_PLURAL,
                namespace=self.cluster.namespace,
                name=task_id,
            )
        except client.rest.ApiException as e:
            if e.status != 404:
                print('!! error deleting IngressRoute:', e)
