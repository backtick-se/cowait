import os
import os.path
import yaml
import docker
from .utils import find_file_in_parents
from .const import CONTEXT_FILE_NAME

client = docker.from_env()


class PipelineContext(object):
    def __init__(self, root_path: str, definition: dict, path: str = None):
        self.root_path = root_path
        self.path = root_path if path is None else path
        self.definition = definition

    def __getitem__(self, key: str) -> any:
        return self.get(key, required=True)

    def get(self, key: str, default: any = None, required: bool = True):
        path = key.split('.')
        value = self.definition
        for part in path:
            if not isinstance(value, dict) or part not in value:
                value = None
                break
            value = value.get(part, default)
        if value is None:
            if default is None and required:
                raise KeyError()
            return default
        return value

    def file(self, file_name: str) -> str:
        """ Find a file within the task context and return its full path """
        return find_file_in_parents(self.path, file_name)

    def file_rel(self, file_name: str) -> str:
        """
        Find a file within the task context and return its relative path
        """
        abs_path = self.file(file_name)
        if not abs_path:
            return None
        return self.relpath(abs_path)

    def relpath(self, context_path: str):
        """ Returns a path relative to the context root """
        return os.path.relpath(context_path, self.root_path)

    def includes(self, path: str) -> bool:
        """ Checks if the path is included in the context """
        return self.root_path in path

    def coalesce(self, key: str, value: any, default: any) -> any:
        if value is not None:
            return value
        return self.get(key, default, required=False)

    def cwd(self, path: str) -> None:
        """
        Navigate within the context. Returns a new context.
        """
        new_path = os.path.abspath(os.path.join(self.path, path))

        if not os.path.isdir(new_path):
            raise RuntimeError(f'Target directory {new_path} does not exist')

        if not self.includes(new_path):
            raise RuntimeError(f'Target path is outside context directory')

        return PipelineContext(
            path=new_path,
            root_path=self.root_path,
            definition=self.definition,
        )

    def get_task_image(self, task):
        repo = self['repo']
        return f'{repo}/{task}:latest'

    @staticmethod
    def open(path: str = None):
        # if no path is provided, open at the current directory
        if not path:
            path = os.getcwd()

        # ensure path is absolute
        path = os.path.abspath(path)

        # ensure the provided path is an actual directory
        if not os.path.isdir(path):
            raise RuntimeError(f'Invalid context path {path}: Not a directory')

        # find context root by looking for the context definition file
        context_file_path = find_file_in_parents(path, CONTEXT_FILE_NAME)
        if context_file_path is None:
            raise RuntimeError(
                f'Could not find {CONTEXT_FILE_NAME} '
                f'in {path} or any of its parent directories.')

        # load context yaml definition
        with open(context_file_path, 'r') as context_file:
            context_def = yaml.load(context_file, Loader=yaml.FullLoader)
            if 'version' not in context_def or context_def['version'] != 1:
                raise RuntimeError('Invalid pipeline context version')

            context = context_def.get('pipeline', {})

        # context root path is the yml folder
        root_path = os.path.dirname(context_file_path)

        return PipelineContext(
            path=path,
            root_path=root_path,
            definition=context,
        )
