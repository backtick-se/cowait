from ..const import DEFAULT_PROVIDER
from ..context import PipelineContext
from ..utils import get_context_cluster
from pipeline.engine import get_cluster_provider


def destroy(provider: str) -> None:
    context = PipelineContext.open()

    # grab cluster provider
    cluster = get_cluster_provider(
        type=context.coalesce('cluster.type', provider, DEFAULT_PROVIDER),
        args=context.get('cluster', {}),
    )

    # kill all tasks
    cluster.destroy_all()


def list_tasks(provider: str) -> None:
    context = PipelineContext.open()
    cluster = get_context_cluster(context, provider)

    tasks = cluster.list_all()
    for task in tasks:
        print(task)
