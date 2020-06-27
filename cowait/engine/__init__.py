# flake8: noqa: F401

from .const import *
from .cluster import ClusterProvider
from .docker import DockerProvider
from .kubernetes import KubernetesProvider
from .api import ApiProvider
from .errors import TaskCreationError, ProviderError
from .utils import env_pack, env_unpack


def get_cluster_provider(type, **args):
    if type == 'docker':
        return DockerProvider(args)
    elif type == 'kubernetes':
        return KubernetesProvider(args)
    elif type == 'api':
        return ApiProvider(args)
    else:
        raise ValueError(f'Unknown cluster provider: {type}')
