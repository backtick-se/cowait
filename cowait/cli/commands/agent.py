import sys
from cowait.tasks import TaskDefinition
from cowait.engine.errors import TaskCreationError
from cowait.utils.const import DEFAULT_BASE_IMAGE
from cowait.utils import uuid
from ..context import CowaitContext
from ..utils import ExitTrap, get_context_cluster, printheader


def agent(provider: str, detach: bool) -> None:
    context = CowaitContext.open()
    cluster = get_context_cluster(context, provider)

    cluster.destroy('agent')

    # create task definition
    taskdef = TaskDefinition(
        id='agent',
        name='cowait.tasks.agent',
        image=DEFAULT_BASE_IMAGE,
        routes={
            '/': 80,
        },
        meta={
            'http_token': uuid(),
        },
    )

    # submit task to cluster
    try:
        task = cluster.spawn(taskdef)
    except TaskCreationError as e:
        printheader('error')
        print('Error creating task:', str(e))
        printheader()
        return

    if detach:
        printheader('detached')
        return

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
