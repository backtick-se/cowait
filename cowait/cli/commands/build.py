import os.path
import sys
import docker.errors
import docker.credentials.errors
from cowait.utils.const import DEFAULT_BASE_IMAGE
from ..task_image import TaskImage
from ..context import CowaitContext
from ..utils import printheader, parse_path


def build(task_path: str = None, image_runtime_path: str = None) -> TaskImage:
    try:
        context = CowaitContext.open(parse_path(task_path), parse_path(image_runtime_path))    
        image = TaskImage.open(context)
        print('context path:', context.root_path)
        print('context image_runtime_path:', context.image_runtime_path)
        print('image:', image.name)

        # find task-specific requirements.txt
        # if it exists, it will be copied to the container, and installed
        requirements = context.file_rel_image_runtime_path('requirements.txt')
        if requirements:
            print('found custom requirements.txt')

        # find custom Dockerfile
        # if it exists, build and extend that instead of the default base image
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
            base_image = base.id

        print('building task image...')
        logs = image.build(
            base=base_image,
            requirements=requirements,
        )

        for log in logs:
            if 'stream' in log:
                print(log['stream'], flush=True, end='')

        return image

    except docker.errors.DockerException as e:
        printheader('error')
        print('Docker exception:', str(e))
