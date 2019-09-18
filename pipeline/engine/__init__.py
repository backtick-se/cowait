from .task import TaskDefinition, TaskContext
from .cluster import ClusterProvider
from .docker import DockerProvider
from .kubernetes import KubernetesProvider

def get_cluster_provider(provider):
    if provider == 'docker':
        return DockerProvider
    elif provider == 'kubernetes':
        return KubernetesProvider
    else:
        raise RuntimeError(f'Unknown cluster provider: {provider}')

