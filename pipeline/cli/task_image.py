import os
import docker
from .const import DEFAULT_BASE_IMAGE
from .context import PipelineContext

client = docker.from_env()


class TaskImage(object):
    def __init__(self, context, name, task_path, base_image=None):
        self.context = context
        self.name = name
        self.path = task_path
        self.base = base_image if base_image else DEFAULT_BASE_IMAGE
        self.image = None

    def build_custom_base(self, dockerfile):
        """ Build a custom image and set it as the base image for this task """
        custom_base, logs = client.images.build(
            path=os.path.dirname(dockerfile),
            dockerfile='Dockerfile',
        )
        self.base = custom_base.id
        return logs

    def build(self, requirements=None):
        """ Build task image """

        # create temporary dockerfile
        df_path = os.path.join(self.context.path, '__dockerfile__')
        with open(df_path, 'w') as df:
            # extend base image
            print(f'FROM {self.base}', file=df)

            # install task-specific requirements
            if requirements:
                print(
                    f'COPY ./{requirements} ./task_requirements.txt', file=df)
                print('RUN pip install -r ./task_requirements.txt', file=df)

            # copy source code
            print('COPY . .', file=df)

        # build image
        self.image, logs = client.images.build(
            path=self.context.path,
            dockerfile=df_path,
        )

        # remove temproary dockerfile
        os.unlink(df_path)

        self.image.tag(
            repository='johanhenriksson/pipeline',
            tag=self.name,
        )

        return logs

    def push(self, repository):
        """ Push task image to a repository """
        if not self.image:
            raise RuntimeError('Task must be built first')

        self.image.tag(
            repository=repository,
            tag=self.name,
        )

        logs = client.images.push(
            repository=repository,
            tag=self.name,
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
    def open(context: PipelineContext, task_name: str):
        task_parts = task_name.split('.')
        task_path = os.path.join(context.path, *task_parts)

        # ensure directory exists
        if not os.path.isdir(task_path):
            raise FileNotFoundError(f'Task directory not found at {task_path}')

        return TaskImage(
            context=context,
            name=task_name,
            task_path=task_path,
        )
