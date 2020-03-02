import sys
from ..const import DEFAULT_BASE_IMAGE
from ..context import PipelineContext
from ..utils import ExitTrap, get_context_cluster, printheader
from pipeline.tasks import TaskDefinition


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
            1337: 1337,
        },
        routes={
            '/': 80,
            '/ws': 1337,
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
