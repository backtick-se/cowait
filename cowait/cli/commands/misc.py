from ..config import Config
from ..context import Context
from cowait.engine import ProviderError


def destroy(config: Config, *, cluster_name: str = None) -> None:
    try:
        context = Context.open(config)
        cluster = context.get_cluster(cluster_name)
        cluster.destroy_all()

    except ProviderError as e:
        print('Provider error:', str(e))


def list_tasks(config: Config, *, cluster_name: str = None) -> None:
    try:
        context = Context.open(config)
        cluster = context.get_cluster(cluster_name)
        tasks = cluster.list_all()
        for task in tasks:
            print(task)

    except ProviderError as e:
        print('Provider error:', str(e))


def kill(config: Config, partial_task_id: str):
    """ Kills all tasks that somewhat matches partial_task_id """
    try:
        cluster = config.get_cluster()
        tasks = cluster.list_all()
        for task in tasks:
            if partial_task_id in str(task):
                cluster.destroy(str(task))
                print('killed ', str(task))

    except ProviderError as e:
        print('Provider error:', str(e))
