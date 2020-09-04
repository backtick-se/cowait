import os.path
import docker
import docker.errors
import docker.credentials.errors
from cowait.utils.const import DEFAULT_BASE_IMAGE
from ..task_image import TaskImage, BuildError
from ..docker_file import Dockerfile
from ..context import CowaitContext, CONTEXT_FILE_NAME
from ..logger import Logger


def build(quiet: bool = False, workdir: str = None, image_name: str = None) -> TaskImage:
    logger = Logger(quiet)
    try:
        if not CowaitContext.exists():
            logger.println(f'No {CONTEXT_FILE_NAME} found. '
                           f'Using default image: {DEFAULT_BASE_IMAGE}')
            return TaskImage.get(DEFAULT_BASE_IMAGE)

        context = CowaitContext.open()
        context.override('workdir', workdir)

        if image_name is not None:
            context.override('image', image_name)

        image = TaskImage.open(context)
        logger.header('BUILD')
        logger.println('Image:', image.name)
        logger.println('Context Root:', context.root_path)
        logger.println('Workdir:', context.workdir)

        # find task-specific requirements.txt
        # if it exists, it will be copied to the container, and installed
        requirements = context.file_rel('requirements.txt')
        if requirements:
            logger.println('* Found custom requirements.txt')

        # find custom Dockerfile
        # if it exists, build and extend that instead of the default base image
        base_image = context.base
        dockerfile = context.file('Dockerfile')
        if dockerfile:
            logger.println('* Found custom Dockerfile:', context.relpath(dockerfile))
            logger.header('BASE')

            basedf = Dockerfile.read(dockerfile)
            base = TaskImage.build_image(
                path=os.path.dirname(dockerfile),
                dockerfile=str(basedf),
            )
            if base is None:
                raise RuntimeError('Failed to build base image')
            base_image = base.id

        logger.header('IMAGE')
        image.build(
            base=base_image,
            requirements=requirements,
            quiet=quiet,
        )

        return image

    except docker.errors.DockerException as e:
        logger.print_exception(f'Docker exception: {e}')

    except BuildError as e:
        logger.print_exception(str(e))
