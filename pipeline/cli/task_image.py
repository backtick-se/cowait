import os
import docker
from .const import DEFAULT_BASE_IMAGE
from .context import PipelineContext

client = docker.from_env()


class TaskImage(object):
    def __init__(self, name, context):
        self.name = name
        self.context = context

    def build(self, base: str = None, requirements: str = None):
        """ Build task image """

        if base is None or base == 'default':
            base = DEFAULT_BASE_IMAGE

        # create temporary dockerfile
        df_path = os.path.join(self.context.path, '__dockerfile__')
        with open(df_path, 'w') as df:
            # extend base image
            print(f'FROM {base}', file=df)

            # install task-specific requirements
            if requirements:
                print(
                    f'COPY ./{requirements} ./task_requirements.txt', file=df)
                print('RUN pip install -r ./task_requirements.txt', file=df)

            # copy source code
            print('COPY . .', file=df)

        # build image
        self.image, logs = self.build_image(
            path=self.context.path,
            dockerfile=df_path,
        )

        # remove temproary dockerfile
        os.unlink(df_path)

        # always tag image so that it works locally
        self.image.tag(
            repository=self.get_image_name(),
            tag='latest'
        )

        return logs

    def get_image_name(self):
        repository = self.context['repo']
        return f'{repository}/{self.name}'

    def push(self):
        """ Push task image to a repository """
        if not self.image:
            raise RuntimeError('Task must be built first')

        self.image.tag(
            repository=self.get_image_name(),
            tag='latest',
        )

        logs = client.images.push(
            repository=self.get_image_name(),
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
    def open(task_name: str, context: PipelineContext = None):
        # automatically create context
        if context is None:
            context = PipelineContext.open()

        task_parts = task_name.split('.')
        task_path = os.path.join(context.root_path, *task_parts)
        context = context.cwd(task_path)

        return TaskImage(
            name=task_name,
            context=context,
        )

    @staticmethod
    def build_image(**kwargs):
        return client.images.build(**kwargs)
