from .const import *
from .cluster import ClusterProvider
from .docker import DockerProvider
from .kubernetes import KubernetesProvider


def get_cluster_provider(type, args = { }):
    if type == 'docker':
        return DockerProvider(args)
    elif type == 'kubernetes':
        return KubernetesProvider(args)
    else:
        raise RuntimeError(f'Unknown cluster provider: {type}')
