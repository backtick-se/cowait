import sys
from ..const import DEFAULT_BASE_IMAGE, DEFAULT_PROVIDER
from ..context import PipelineContext
from ..utils import ExitTrap, get_context_cluster, printheader
from pipeline.engine import get_cluster_provider
from pipeline.tasks import TaskDefinition


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


def agent(provider: str) -> None:
    context = PipelineContext.open()
    cluster = get_context_cluster(context, provider)

    cluster.destroy('agent')

    # create task definition
    taskdef = TaskDefinition(
        id='agent',
        name='pipeline.tasks.agent',
        image=DEFAULT_BASE_IMAGE,
        ports={
            '1337': '1337',
            '1338': '1338',
        },
    )

    task = cluster.spawn(taskdef)

    def destroy(*args):
        print()
        printheader('interrupt')
        cluster.destroy(task.id)
        sys.exit(0)

    with ExitTrap(destroy):
        # capture & print logs
        logs = cluster.logs(task)
        printheader('task output')
        for log in logs:
            print(log, flush=True)
