import os
import os.path
import docker
from .context import Context
from .docker_file import Dockerfile

client = docker.from_env()


class BuildError(RuntimeError):
    pass


class TaskImage(object):
    def __init__(self, context):
        self.context = context
        self.image = None

    @property
    def name(self):
        return self.context.image

    def build(self, base: str, requirements: str = None, buildargs: dict = {}, quiet: bool = False) -> None:
        """ Build task image """

        # create temporary dockerfile
        df = Dockerfile(base)

        # install task-specific requirements
        requirements = self.context.file_rel('requirements.txt')
        if requirements:
            df.copy(f'./{requirements}', './requirements.txt')
            df.run('pip install -r ./requirements.txt')

        # copy source code
        df.copy('.', '.')

        workdir = self.context.workdir
        if workdir != '.':
            df.workdir(os.path.join('/var/task', workdir))

        self.image = TaskImage.build_image(
            dockerfile=str(df),
            path=self.context.root_path,
            tag=f'{self.name}:latest',
            buildargs=buildargs,
            quiet=quiet,
        )

        # tag the image
        self.image.tag(
            repository=self.name,
            tag='latest',
        )

    def push(self):
        """
        Push context image to a remote registry.
        """
        logs = client.images.push(
            repository=self.name,
            tag='latest',
            stream=True
        )
        return logs

    @staticmethod
    def open(context: Context = None):
        # automatically create context
        if context is None:
            context = Context.open()

        return TaskImage(
            context=context,
        )

    @staticmethod
    def get(name_or_id):
        return client.images.get(name_or_id)

    @staticmethod
    def build_image(quiet: bool, **kwargs):
        logs = client.api.build(decode=True, rm=True, **kwargs)

        image_hash = None
        for log in logs:
            if 'stream' in log:
                if not quiet:
                    print(log['stream'], end='', flush=True)
            elif 'aux' in log and 'ID' in log['aux']:
                image_hash = log['aux']['ID']
            elif 'errorDetail' in log:
                raise BuildError(log['errorDetail']['message'])
            else:
                if not quiet:
                    print(log)

        if image_hash is not None:
            return TaskImage.get(image_hash)
