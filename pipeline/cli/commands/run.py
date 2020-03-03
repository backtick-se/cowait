import os
import sys
from pipeline.tasks import TaskDefinition
from pipeline.engine.errors import TaskCreationError
from ..context import PipelineContext
from ..utils import ExitTrap, get_context_cluster, printheader
from ..const import DEFAULT_REPO
from .push import push


def run(
    task: str,
    provider: str,
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
    context = PipelineContext.open()
    cluster = get_context_cluster(context, provider)

    # figure out image name
    image = None
    if '/' in task:
        s = task.rfind('/')
        image = task[:s]
        task = task[s+1:]
        if '/' not in image:
            # prepend default repo
            image = f'{DEFAULT_REPO}/{image}'
    else:
        if build:
            push()
        image = context.get_image_name()

    # default to agent as upstream
    agent = cluster.find_agent()

    # create task definition
    taskdef = TaskDefinition(
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
