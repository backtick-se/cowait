from ..const import DEFAULT_PROVIDER
from ..context import CowaitContext
from ..utils import get_context_cluster
from cowait.engine import get_cluster_provider, ProviderError


def destroy(provider: str) -> None:
    try:
        context = CowaitContext.open()

        # grab cluster provider
        cluster = get_cluster_provider(
            type=context.coalesce('cluster.type', provider, DEFAULT_PROVIDER),
            args=context.get('cluster', {}),
        )

        # kill all tasks
        cluster.destroy_all()

    except ProviderError as e:
        print('Provider error:', str(e))


def list_tasks(provider: str) -> None:
    try:
        context = CowaitContext.open()
        cluster = get_context_cluster(context, provider)

        tasks = cluster.list_all()
        for task in tasks:
            print(task)

    except ProviderError as e:
        print('Provider error:', str(e))


def kill(task_id: str, provider: str):
    try:
        context = CowaitContext.open()
        cluster = get_context_cluster(context, provider)
        cluster.destroy(task_id)

    except ProviderError as e:
        print('Provider error:', str(e))
