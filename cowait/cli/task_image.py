import os
import docker
from .context import CowaitContext

client = docker.from_env()


class TaskImage(object):
    def __init__(self, context):
        self.context = context

    @property
    def name(self):
        return self.context.get_image_name()

    def build(self, base, requirements: str = None):
        """ Build task image """

        # create temporary dockerfile
        df_path = os.path.join(self.context.root_path, '__dockerfile__')
        with open(df_path, 'w') as df:
            # extend base image
            print(f'FROM {base}', file=df)

            # install task-specific requirements
            requirements = self.context.file_rel('requirements.txt')
            if requirements:
                print(f'COPY ./{requirements} ./requirements.txt', file=df)
                print('RUN pip install -r ./requirements.txt', file=df)

            # copy source code
            print('COPY . .', file=df)

        # build image
        self.image, logs = self.build_image(
            path=self.context.root_path,
            dockerfile=df_path,
        )

        # remove temproary dockerfile
        os.unlink(df_path)

        # always tag image so that it works locally
        # todo: probably does not work until after logs
        self.image.tag(
            repository=self.name,
            tag='latest'
        )

        return logs

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
        return client.images.build(**kwargs)
