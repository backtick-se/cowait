import os
import docker
from .context import PipelineContext

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
            print('COPY . context/', file=df)

        # build image
        self.image, logs = self.build_image(
            path=self.context.root_path,
            dockerfile=df_path,
        )

        # remove temproary dockerfile
        os.unlink(df_path)

        # always tag image so that it works locally
        self.image.tag(
            repository=self.name,
            tag='latest'
        )

        return logs

    def push(self):
        """ Push task image to a repository """
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

    def run(self):
        """ Run task in a container """
        if not self.image:
            raise RuntimeError('Task must be built first')

        return client.containers.run(
            image=self.image.id,
            detach=True,
            environment={
                'PYTHONUNBUFFERED': '0',
            },
        )

    @staticmethod
    def open(context: PipelineContext = None):
        # automatically create context
        if context is None:
            context = PipelineContext.open()

        # find task folder path
        """
        task_parts = task_name.split('.')
        split_idx = len(task_parts) - 1
        for i, part in enumerate(task_parts):
            if part[0].isupper():
                split_idx = i
                break

        task_path = os.path.join(context.root_path, *task_parts[:split_idx])
        context = context.cwd(task_path)
        """

        return TaskImage(
            context=context,
        )

    @staticmethod
    def build_image(**kwargs):
        return client.images.build(**kwargs)
