from cowait.engine import ProviderError
from ..config import Config
from ..context import Context
from .run import RunLogger


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
            print(task.id)

    except ProviderError as e:
        print('Provider error:', str(e))


def kill(config: Config, partial_task_id: str, cluster_name: str):
    """ Kills all tasks that somewhat matches partial_task_id """
    try:
        context = Context.open(config)
        cluster = context.get_cluster(cluster_name)
        tasks = cluster.list_all()
        for task in tasks:
            if partial_task_id in task.id:
                cluster.destroy(task.id)
                print('killed ', task.id)

    except ProviderError as e:
        print('Provider error:', str(e))


def logs(config: Config, task_id: str, cluster_name: str, raw: bool = False):
    try:
        context = Context.open(config)
        cluster = context.get_cluster(cluster_name)

        logs = cluster.logs(task_id)
        logger = RunLogger(raw)
        logger.id = task_id
        logger.header('task output')
        for msg in logs:
            logger.handle(msg)
        logger.finalize()

        logger.header()

    except ProviderError as e:
        print('Provider error:', str(e))
