import os
from ..context import CowaitContext
from ..utils import ExitTrap, get_context_cluster, printheader
from cowait.tasks import TaskDefinition
from .build import build as run_build
from .push import push as run_push


def test(
    provider: str,
    push: bool,
):
    context = CowaitContext.open()
    cluster = get_context_cluster(context, provider)

    if push:
        run_push()
    else:
        run_build()

    # execute the test task within the current image
    task = cluster.spawn(TaskDefinition(
        name='cowait.test',
        image=context.get_image_name(),
    ))

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
