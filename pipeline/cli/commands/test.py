import os
from ..context import PipelineContext
from ..utils import ExitTrap, get_context_cluster, printheader
from pipeline.tasks import TaskDefinition
from .build import build as run_build
from .push import push as run_push


def test(
    provider: str,
    push: bool,
):
    context = PipelineContext.open()
    cluster = get_context_cluster(context, provider)

    if push:
        print('building & pushing image...')
        run_push()
    else:
        print('building image...')
        run_build()

    # create task definition
    taskdef = TaskDefinition(
        name='pipeline.tasks.shell',
        image=context.get_image_name(),
        inputs={
            'command': 'python -m pytest context/',
        },
    )

    task = cluster.spawn(taskdef)

    def destroy(*args):
        print()
        printheader('interrupt')
        cluster.destroy(task.id)
        os._exit(1)

    with ExitTrap(destroy):
        # capture & print logs
        logs = cluster.logs(task)
        printheader('task output')
        for log in logs:
            print(log, flush=True)
