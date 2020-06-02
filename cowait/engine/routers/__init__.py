# flake8: noqa: F401

from .router import Router
from .local_port_router import LocalPortRouter
from .traefik_router import TraefikRouter
from .traefik2_router import Traefik2Router


def create_router(cluster, kind: str = 'none'):
    if kind == 'none':
        return Router(cluster)
    if kind == 'local':
        return LocalPortRouter(cluster)
    if kind == 'traefik':
        return TraefikRouter(cluster)
    if kind == 'traefik2':
        return Traefik2Router(cluster)
    
    raise RuntimeError(f'Unknown router type {kind}')
