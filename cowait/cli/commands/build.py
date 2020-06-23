import os.path
import docker.errors
import docker.credentials.errors
from cowait.utils.const import DEFAULT_BASE_IMAGE
from ..task_image import TaskImage
from ..context import CowaitContext
from ..logger import Logger


def build(quiet: bool = False) -> TaskImage:
    logger = Logger(quiet)
    try:
        context = CowaitContext.open()
        image = TaskImage.open(context)
        logger.header('BUILD')
        logger.println('Image:', image.name)
        logger.println('Context Root:', context.root_path)

        # find task-specific requirements.txt
        # if it exists, it will be copied to the container, and installed
        requirements = context.file_rel('requirements.txt')
        if requirements:
            logger.print('* Found custom requirements.txt')

        # find custom Dockerfile
        # if it exists, build and extend that instead of the default base image
        base_image = context.get('base', DEFAULT_BASE_IMAGE)
        dockerfile = context.file('Dockerfile')
        if dockerfile:
            logger.print('* Found custom Dockerfile:', context.relpath(dockerfile))
            logger.header('BASE')

            base, logs = TaskImage.build_image(
                path=os.path.dirname(dockerfile),
                dockerfile='Dockerfile',
            )
            for log in logs:
                if 'stream' in log and not quiet:
                    print(log['stream'], flush=True, end='')
            base_image = base.id

        logger.header('IMAGE')
        logs = image.build(
            base=base_image,
            requirements=requirements,
        )

        for log in logs:
            if 'stream' in log and not quiet:
                print(log['stream'], flush=True, end='')

        logger.header()
        return image

    except docker.errors.DockerException as e:
        logger.print_exception(f'Docker exception: {e}')
