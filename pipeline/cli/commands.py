import sys
import json
import os.path
from .const import DEFAULT_BASE_IMAGE, DEFAULT_PROVIDER
from .task_image import TaskImage
from .context import PipelineContext
from .utils import ExitTrap
from ..engine import get_cluster_provider
from ..tasks import TaskDefinition

HEADER_WIDTH = 80


def printheader(title: str = None) -> None:
    if title is None:
        print(f'--'.ljust(HEADER_WIDTH, '-'))
    else:
        print(f'-- {title} '.upper().ljust(HEADER_WIDTH, '-'))


def get_context_cluster(context, provider: str = None):
    return get_cluster_provider(
        type=context.coalesce('cluster.type', provider, DEFAULT_PROVIDER),
        args=context.get('cluster', {}),
    )


def build(task: str) -> TaskImage:
    image = TaskImage.open(task)
    print('context path:', image.context.root_path)
    print('task path:', image.context.relpath(image.context.path))

    # find task-specific requirements.txt
    # if it exists, it will be copied to the container, and installed
    requirements = image.context.file_rel('requirements.txt')
    if requirements:
        print('found custom requirements.txt:', requirements)

    # find custom Dockerfile
    # if it exists, build it and extend that instead of the default base image
    base_image = DEFAULT_BASE_IMAGE
    dockerfile = image.context.file('Dockerfile')
    if dockerfile:
        print('found custom Dockerfile:', image.context.relpath(dockerfile))
        print('building custom base image...')

        base, logs = TaskImage.build_image(
            path=os.path.dirname(dockerfile),
            dockerfile='Dockerfile',
        )
        for log in logs:
            if 'stream' in log:
                print(log['stream'], flush=True, end='')

    print('building task image...')
    logs = image.build(
        base=base_image,
        requirements=requirements,
    )

    for log in logs:
        if 'stream' in log:
            print(log['stream'], flush=True, end='')

    return image


def run(
    task: str,
    provider: str,
    inputs: dict = {},
    config: dict = {},
    env: dict = {},
    build: bool = False,
    upstream: str = None,
    detach: bool = False,
):
    if build:
        push(task)

    context = PipelineContext.open()
    cluster = get_context_cluster(context, provider)
    image = context.get_task_image(task)

    # create task definition
    taskdef = TaskDefinition(
        name=task,
        image=image,
        config={
            **context.get('worker', {}),
            **config,
        },
        inputs=inputs,
        env={
            **context.get('environment', {}),
            **env,
        },
        namespace='default',
        upstream=context.coalesce('upstream', upstream, None),
        parent=None,  # root task
    )

    # print execution info
    printheader('task')
    print('   task:      ', taskdef.id)
    print('   provider:  ', provider)
    if upstream:
        print('   upstream:  ', upstream)
    print('   image:     ', image)
    print('   inputs:    ', inputs)
    print('   env:       ', env)

    # submit task to cluster
    task = cluster.spawn(taskdef)

    if detach:
        print('~~ running in detached mode')
        printheader()
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


def push(task: str) -> TaskImage:
    image = build(task)

    sys.stdout.write('pushing...')
    logs = image.push()
    progress = {}
    for log in logs:
        rows = log.decode('utf-8').split('\r\n')
        for data in rows:
            if len(data) == 0:
                continue
            update = json.loads(data.strip())
            if 'id' in update and 'progressDetail' in update:
                id = update['id']
                progress[id] = update['progressDetail']

        current = 0
        total = 0
        for detail in progress.values():
            current += detail.get('current', 0)
            total += detail.get('total', 0)

        if total > 0:
            pct = 100 * min(current / total, 1.0)
            sys.stdout.write(f'\rpushing... {pct:0.2f}%')
            sys.stdout.flush()

    sys.stdout.write(f'\rpushing... done     \n')
    sys.stdout.flush()
    return image


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

    # create task definition
    taskdef = TaskDefinition(
        id='agent',
        name='tasks.agent',
        image=DEFAULT_BASE_IMAGE,
        namespace='default',
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
