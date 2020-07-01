from ..config import CowaitConfig
from cowait.engine import ProviderError


def destroy(config: CowaitConfig) -> None:
    try:
        cluster = config.get_cluster()
        cluster.destroy_all()

    except ProviderError as e:
        print('Provider error:', str(e))


def list_tasks(config: CowaitConfig) -> None:
    try:
        cluster = config.get_cluster()
        tasks = cluster.list_all()
        for task in tasks:
            print(task)

    except ProviderError as e:
        print('Provider error:', str(e))


def kill(config: CowaitConfig, task_id: str):
    try:
        cluster = config.get_cluster()
        cluster.destroy(task_id)

    except ProviderError as e:
        print('Provider error:', str(e))
