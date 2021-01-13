import os
import os.path
import sys
import json
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

    @staticmethod
    def pull(name: str, tag: str = 'latest') -> None:
        try:
            # if the image already exists, just return it
            # todo: add a policy setting for this, similar to kubernetes
            return TaskImage.get(f'{name}:{tag}')
        except docker.errors.ImageNotFound:
            # we expect this error. pull the image
            pass

        logs = client.api.pull(repository=name, tag=tag, stream=True, decode=True)
        sys.stdout.write('   pulling image...')
        sys.stdout.flush()

        progress = {}
        for update in logs:
            if 'id' in update and 'progressDetail' in update:
                id = update['id']
                progress[id] = update['progressDetail']
            if 'errorDetail' in update:
                print('\rError:', update['error'])
                return

            current = 0
            total = 0
            for detail in progress.values():
                current += detail.get('current', 0)
                total += detail.get('total', 0)

            if total > 0:
                pct = 100 * min(current / total, 1.0)
                sys.stdout.write(f'\r   pulling image... {pct:0.2f}%  ')
                sys.stdout.flush()

        sys.stdout.write('\r   pulling image... done   \n')
        sys.stdout.flush()

