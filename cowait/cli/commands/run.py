import os
import sys
from cowait.tasks import TaskDefinition
from cowait.engine.errors import TaskCreationError
from cowait.utils import parse_task_image_name
from ..context import CowaitContext
from ..utils import ExitTrap, get_context_cluster, printheader
from .build import build as build_cmd


def run(
    task: str,
    provider: str,
    name: str = None,
    inputs: dict = {},
    env: dict = {},
    ports: dict = {},
    routes: dict = {},
    build: bool = False,
    upstream: str = None,
    detach: bool = False,
    cpu: str = '0',
    memory: str = '0',
):
    context = CowaitContext.open()
    cluster = get_context_cluster(context, provider)

    # figure out image name
    image, task = parse_task_image_name(task, None)
    if image is None:
        if build:
            build_cmd()
        image = context.get_image_name()

    # default to agent as upstream
    agent = cluster.find_agent()

    # create task definition
    taskdef = TaskDefinition(
        id=name,
        name=task,
        image=image,
        inputs=inputs,
        env={
            **context.get('environment', {}),
            **env,
        },
        ports=ports,
        routes=routes,
        upstream=context.coalesce('upstream', upstream, agent),
        parent=None,  # root task
        owner=os.getlogin(),
        cpu=cpu,
        memory=memory,
    )

    # print execution info
    printheader('task')
    print('   task:      ', taskdef.id)
    print('   provider:  ', provider)
    if taskdef.upstream:
        print('   upstream:  ', taskdef.upstream)
    print('   image:     ', image)
    print('   inputs:    ', inputs)
    print('   env:       ', env)

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

    printheader()
