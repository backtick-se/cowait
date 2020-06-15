import os
import os.path
import docker
from .context import CowaitContext

client = docker.from_env()

# shim that allows passing dockerfiles as a string together with a context path.
# this removes the need to write temporary files!
# source: https://github.com/docker/docker-py/issues/2105
docker.api.build.process_dockerfile = lambda dockerfile, path: ('Dockerfile', dockerfile)


class Dockerfile(object):
    def __init__(self, base):
        self.lines = [f'FROM {base}']

    def copy(self, src, dst):
        self.lines.append(f'COPY {src} {dst}')

    def run(self, cmd):
        self.lines.append(f'RUN {cmd}')

    def workdir(self, path):
        self.lines.append(f'WORKDIR {path}')

    def __str__(self):
        return '\n'.join(self.lines)


class BuildError(RuntimeError):
    pass


class TaskImage(object):
    def __init__(self, context):
        self.context = context

    @property
    def name(self):
        return self.context.get_image_name()

    def build(self, base: str, requirements: str = None):
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

        return TaskImage.build_image(
            dockerfile=str(df),
            path=self.context.root_path,
            tag=f'{self.name}:latest',
        )

    def push(self):
        """
        Push context image to a remote registry.
        """
        if not self.image:
            raise RuntimeError('Task must be built first')

        self.image.tag(
            repository=self.name,
            tag='latest',
        )

        logs = client.images.push(
            repository=self.name,
            tag='latest',
            stream=True
        )
        return logs

    @staticmethod
    def open(context: CowaitContext = None):
        # automatically create context
        if context is None:
            context = CowaitContext.open()

        return TaskImage(
            context=context,
        )

    @staticmethod
    def build_image(**kwargs):
        logs = client.api.build(decode=True, rm=True, **kwargs)

        image_hash = None
        for log in logs:
            if 'stream' in log:
                print(log['stream'], end='', flush=True)
            elif 'aux' in log and 'ID' in log['aux']:
                image_hash = log['aux']['ID']
            elif 'errorDetail' in log:
                raise BuildError(log['errorDetail']['message'])
            else:
                print(log)

        if image_hash is not None:
            return client.images.get(image_hash)
