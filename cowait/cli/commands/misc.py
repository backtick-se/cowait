from ..config import CowaitConfig
from ..context import CowaitContext
from cowait.engine import ProviderError


def destroy(cluster_name: str = None) -> None:
    try:
        config = CowaitConfig.load()
        context = CowaitContext.open()

        # setup cluster provider
        if cluster_name is None:
            cluster_name = context.get('cluster', config.default_cluster)
        cluster = config.get_cluster(cluster_name)

        # kill all tasks
        cluster.destroy_all()

    except ProviderError as e:
        print('Provider error:', str(e))


def list_tasks(cluster_name: str = None) -> None:
    try:
        config = CowaitConfig.load()
        context = CowaitContext.open()

        # setup cluster provider
        if cluster_name is None:
            cluster_name = context.get('cluster', config.default_cluster)
        cluster = config.get_cluster(cluster_name)

        tasks = cluster.list_all()
        for task in tasks:
            print(task)

    except ProviderError as e:
        print('Provider error:', str(e))


def kill(task_id: str, cluster_name: str = None):
    try:
        config = CowaitConfig.load()
        context = CowaitContext.open()

        # setup cluster provider
        if cluster_name is None:
            cluster_name = context.get('cluster', config.default_cluster)
        cluster = config.get_cluster(cluster_name)

        cluster.destroy(task_id)

    except ProviderError as e:
        print('Provider error:', str(e))
