import os.path
from .task_image import TaskImage
from .context import PipelineContext
from ..engine import get_cluster_provider
from ..tasks import TaskDefinition

HEADER_WIDTH = 80


def printheader(title: str = None):
    if title is None:
        print(f'--'.ljust(HEADER_WIDTH, '-'))
    else:
        print(f'-- {title}: '.upper().ljust(HEADER_WIDTH, '-'))


def build(task: str) -> TaskImage:
    context = PipelineContext.open()
    image = TaskImage.open(context, task)
    print('context path:', context.path)

    # find task-specific requirements.txt
    # if it exists, it will be copied to the container, and installed
    requirements = context.file_rel('requirements.txt')
    if requirements:
        print('found custom requirements.txt:', requirements)

    # find custom Dockerfile
    # if it exists, build it and extend that instead of the default base image
    dockerfile = context.file('Dockerfile')
    if dockerfile:
        print('found custom Dockerfile:',
              os.path.relpath(dockerfile, image.root))
        print('building custom base image...')
        logs = image.build_custom_base(dockerfile)
        for log in logs:
            if 'stream' in log:
                print(log['stream'], flush=True, end='')

    print('building task image...')
    logs = image.build(
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
    upstream=None
):
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
