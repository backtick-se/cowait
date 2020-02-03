import sys
import os.path
from .task_image import TaskImage
from .context import PipelineContext
from .utils import ExitTrap
from ..engine import get_cluster_provider
from ..tasks import TaskDefinition

HEADER_WIDTH = 80


def printheader(title: str = None):
    if title is None:
        print(f'--'.ljust(HEADER_WIDTH, '-'))
    else:
        print(f'-- {title} '.upper().ljust(HEADER_WIDTH, '-'))


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
    base_image = 'default'
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
    image = f'johanhenriksson/pipeline-task:{task}'

    # grab cluster provider
    cluster = get_cluster_provider(type=provider)

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
        upstream=upstream,
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

    print('pushing...')
    logs = image.push('johanhenriksson/pipeline-task')
    for _ in logs:
        pass

    print('done')
    return image


def destroy(provider: str) -> None:
    # grab cluster provider
    cluster = get_cluster_provider(type=provider)

    # kill all tasks
    cluster.destroy_all()


def list_tasks(provider: str) -> None:
    # grab cluster provider
    cluster = get_cluster_provider(type=provider)

    tasks = cluster.list_all()
    for task in tasks:
        print(task)
