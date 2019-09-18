import os
from .docker import client
from .utils import find_file_in_parents
from .const import CONTEXT_FILE_NAME, DEFAULT_BASE_IMAGE


class TaskImage(object):
    def __init__(self, name, task_path, root_path, base_image = None):
        self.name = name
        self.path = task_path
        self.root = root_path
        self.base = base_image if base_image else DEFAULT_BASE_IMAGE
        self.image = None


    def find_file(self, file_name):
        """ Find a file within the task context and return its full path """
        return find_file_in_parents(self.path, file_name)


    def find_file_rel(self, file_name):
        """ Find a file within the task context and return its relative path """
        abs_path = self.find_file(file_name)
        if not abs_path:
            return None
        return os.path.relpath(abs_path, self.root)


    def build_custom_base(self, dockerfile):
        """ Build a custom image and set it as the base image for this task """
        custom_base, logs = client.images.build(
            path=os.path.dirname(dockerfile),
            dockerfile='Dockerfile',
        )
        self.base = custom_base.id
        return logs


    def build(self, requirements = None):
        """ Build task image """

        # create temporary dockerfile
        df_path = os.path.join(self.root, '__dockerfile__')
        with open(df_path, 'w') as df:
            # extend base image
            print(f'FROM {self.base}', file=df)

            # copy source code
            print('COPY . .', file=df)

            # install task-specific requirements
            if requirements:
                print(f'COPY ./{requirements} ./requirements.txt', file=df)
                print('RUN pip install -r ./requirements.txt', file=df)

            # run task executor
            print(f'CMD [ "python", "-u", "main.py", "{self.name}" ]', file=df)

        # build image
        self.image, logs = client.images.build(
            path       = self.root,
            dockerfile = df_path,
            rm         = True,
        )

        # remove temproary dockerfile
        os.unlink(df_path)

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
            stream = True
        )
        return logs


    def run(self):
        """ Run task in a container """
        if not self.image:
            raise RuntimeError('Task must be built first')

        return client.containers.run(
            image = self.image.id,
            detach = True,
            environment = {
                'PYTHONUNBUFFERED': '0',
            },
        )


    @staticmethod
    def create(task_name, work_dir = None):
        if not work_dir:
            work_dir = os.getcwd()

        task_parts = task_name.split('.')
        task_path = os.path.join(work_dir, *task_parts)

        # ensure directory exists
        if not os.path.isdir(task_path):
            raise FileNotFoundError(f'Task directory not found at {task_path}')

        # find context file
        context_file = find_file_in_parents(task_path, CONTEXT_FILE_NAME)
        if context_file is None:
            raise RuntimeError(f'Could not find {CONTEXT_FILE_NAME} in {task_path} or any of its parent directories.')

        # context path is the enclosing folder
        root_path = os.path.dirname(context_file)

        return TaskImage(
            name      = task_name,
            task_path = task_path,
            root_path = root_path,
        )