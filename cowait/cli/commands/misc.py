from ..config import CowaitConfig
from ..context import CowaitContext
from cowait.engine import ProviderError


def destroy(config: CowaitConfig) -> None:
    try:
        context = CowaitContext.open()
        cluster_name = context.get('cluster', config.default_cluster)
        cluster = config.get_cluster(cluster_name)

        # kill all tasks
        cluster.destroy_all()

    except ProviderError as e:
        print('Provider error:', str(e))


def list_tasks(config: CowaitConfig) -> None:
    try:
        context = CowaitContext.open()
        cluster_name = context.get('cluster', config.default_cluster)
        cluster = config.get_cluster(cluster_name)

        tasks = cluster.list_all()
        for task in tasks:
            print(task)

    except ProviderError as e:
        print('Provider error:', str(e))


def kill(config: CowaitConfig, task_id: str):
    try:
        context = CowaitContext.open()
        cluster_name = context.get('cluster', config.default_cluster)
        cluster = config.get_cluster(cluster_name)

        cluster.destroy(task_id)

    except ProviderError as e:
        print('Provider error:', str(e))
