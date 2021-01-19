import os.path
import docker
import docker.errors
import docker.credentials.errors
from cowait.utils.const import DEFAULT_BASE_IMAGE
from ..task_image import TaskImage, BuildError
from ..docker_file import Dockerfile
from ..context import Context, CONTEXT_FILE_NAME
from ..config import Config
from ..logger import Logger
from .push import push as push_command


def build(
    config: Config, *,
    image_name: str = None,
    workdir: str = None,
    buildargs: dict = {},
    quiet: bool = False,
    push: bool = False,
) -> TaskImage:
    logger = Logger(quiet)
    try:
        if not Context.exists():
            logger.println(f'No {CONTEXT_FILE_NAME} found. '
                           f'Using default image: {DEFAULT_BASE_IMAGE}')
            return TaskImage.get(DEFAULT_BASE_IMAGE)

        context = Context.open(config)
        context.override('workdir', workdir)

        if image_name is not None:
            context.override('image', image_name)

        image = TaskImage.open(context)
        logger.header('BUILD')
        logger.println('Image:', image.name)
        logger.println('Context Root:', context.root_path)
        logger.println('Workdir:', context.workdir)

        if len(buildargs) > 0:
            logger.println('Buildargs:')
            for arg in buildargs.keys():
                logger.println(f'  {arg}')

        # find task-specific requirements.txt
        # if it exists, it will be copied to the container, and installed
        # custom requirements are ignored when using custom dockerfiles.
        requirements = context.file_rel('requirements.txt')
        if requirements:
            logger.println('* Found custom requirements.txt')

        # find custom Dockerfile
        # if it exists, build and extend that instead of the default base image
        base_image = context.base
        dockerfile = context.file('Dockerfile')
        if dockerfile:
            logger.println('* Found custom Dockerfile:', context.relpath(dockerfile))

            # disable automatic requirements.txt install when using custom dockerfiles.
            # notify user to avoid confusion
            if requirements:
                logger.println('! Warning: requirements.txt is not automatically installed when using custom dockerfiles.')
                requirements = None

            if not os.path.isfile('.dockerignore'):
                logger.println('! Warning: No .dockerignore file found.')

            logger.header('BASE')
            basedf = Dockerfile.read(dockerfile)
            base = TaskImage.build_image(
                path=os.path.dirname(dockerfile),
                dockerfile=str(basedf),
                quiet=quiet,
                buildargs=buildargs,
            )
            if base is None:
                raise RuntimeError('Failed to build base image')
            base_image = base.id

        logger.header('IMAGE')
        image.build(
            base=base_image,
            requirements=requirements,
            quiet=quiet,
            buildargs=buildargs,
        )

        logger.header()

        if push:
            push_command(config)

        return image

    except docker.errors.DockerException as e:
        logger.print_exception(f'Docker exception: {e}')

    except BuildError as e:
        logger.print_exception(str(e))
