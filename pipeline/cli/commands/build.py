import os.path
from ..const import DEFAULT_BASE_IMAGE
from ..task_image import TaskImage
from ..context import PipelineContext


def build() -> TaskImage:
    context = PipelineContext.open()
    image = TaskImage.open(context)
    print('context path:', context.root_path)
    print('image:', image.name)

    # find task-specific requirements.txt
    # if it exists, it will be copied to the container, and installed
    requirements = context.file_rel('requirements.txt')
    if requirements:
        print('found custom requirements.txt:', requirements)

    # find custom Dockerfile
    # if it exists, build it and extend that instead of the default base image
    base_image = context.get('base', DEFAULT_BASE_IMAGE)
    dockerfile = context.file('Dockerfile')
    if dockerfile:
        print('found custom Dockerfile:', context.relpath(dockerfile))
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
