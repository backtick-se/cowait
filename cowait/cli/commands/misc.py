from ..const import DEFAULT_PROVIDER
from ..context import cowaitContext
from ..utils import get_context_cluster
from cowait.engine import get_cluster_provider


def destroy(provider: str) -> None:
    context = cowaitContext.open()

    # grab cluster provider
    cluster = get_cluster_provider(
        type=context.coalesce('cluster.type', provider, DEFAULT_PROVIDER),
        args=context.get('cluster', {}),
    )

    # kill all tasks
    cluster.destroy_all()


def list_tasks(provider: str) -> None:
    context = cowaitContext.open()
    cluster = get_context_cluster(context, provider)

    tasks = cluster.list_all()
    for task in tasks:
        print(task)


def kill(task_id: str, provider: str):
    context = cowaitContext.open()
    cluster = get_context_cluster(context, provider)
    cluster.destroy(task_id)
