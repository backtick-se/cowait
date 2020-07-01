import os
import os.path
import yaml
import docker
from cowait.utils.const import DEFAULT_BASE_IMAGE
from .utils import find_file_in_parents
from .const import CONTEXT_FILE_NAME

client = docker.from_env()


class CowaitContext(object):
    def __init__(self, root_path: str, definition: dict):
        self.root_path = root_path
        self.definition = definition

    def __getitem__(self, key: str) -> any:
        return self.get(key, required=True)

    def __setitem__(self, key: str, value: any):
        self.set(key, value)

    @property
    def workdir(self) -> str:
        return self.get('workdir', '.', False)

    def set(self, key: str, value: any) -> any:
        path = None
        if isinstance(key, str):
            path = key.split('.')
        elif isinstance(key, list):
            path = key
        else:
            raise TypeError("Expected key to be str or list")

        if len(path) < 1:
            raise ValueError(f'Invalid key {key}')

        container = self.definition
        for part in path[:-1]:
            if part not in container:
                container[part] = {}
            container = container[part]

        container[path[-1]] = value
        return value

    def override(self, key: str, value: any) -> any:
        if value is None:
            return self.get(key, None, False)
        return self.set(key, value)

    def get(self, key: str, default: any = None, required: bool = True) -> any:
        path = None
        if isinstance(key, str):
            path = key.split('.')
        elif isinstance(key, list):
            path = key
        else:
            raise TypeError("Expected key to be str or list")

        if len(path) < 1:
            raise ValueError(f'Invalid key {key}')

        value = self.definition
        for part in path:
            if not isinstance(value, dict) or part not in value:
                value = None
                break
            value = value.get(part, default)
        if value is None:
            if default is None and required:
                raise KeyError(f'{key} not set in context')
            return default
        return value

    def file(self, file_name: str) -> str:
        """
        Find a file within the task context and return its full path
        """
        path = os.path.join(self.root_path, self.workdir, file_name)
        if not os.path.isfile(path):
            return None
        return path

    def file_rel(self, file_name: str) -> str:
        """
        Find a file within the task context and return its relative path
        """
        abs_path = self.file(file_name)
        if not abs_path:
            return None
        return self.relpath(abs_path)

    def relpath(self, context_path: str):
        """
        Returns a path relative to the context root
        """
        return os.path.relpath(context_path, self.root_path)

    def includes(self, path: str) -> bool:
        """
        Checks if the path is included in the context
        """
        return self.root_path in path

    def coalesce(self, key: str, value: any, default: any) -> any:
        if value is not None:
            return value
        return self.get(key, default, required=False)

    def get_image_name(self):
        """
        Returns the context image name.
        """
        return self.get('image', DEFAULT_BASE_IMAGE)

    @property
    def image(self):
        return self.get('image', DEFAULT_BASE_IMAGE)

    @staticmethod
    def exists(path: str = None):
        if path is None:
            path = os.getcwd()

        # ensure the provided path is an actual directory
        if not os.path.isdir(path):
            return False

        # find context root by looking for the context definition file
        context_file_path = find_file_in_parents(path, CONTEXT_FILE_NAME)
        return context_file_path is not None

    @staticmethod
    def open(path: str = None):
        if path is None:
            path = os.getcwd()

        # ensure the provided path is an actual directory
        if not os.path.isdir(path):
            raise ValueError(f'Invalid context path {path}: Not a directory')

        context = {
            'image': 'cowait/task',
        }

        # find context root by looking for the context definition file
        context_file_path = find_file_in_parents(path, CONTEXT_FILE_NAME)
        if context_file_path is None:
            # use the current directory as the context
            return CowaitContext(
                root_path=os.path.abspath(path),
                definition=context,
            )

        # load context yaml definition
        with open(context_file_path, 'r') as context_file:
            context_def = yaml.load(context_file, Loader=yaml.FullLoader)
            if context_def is not None:
                if 'version' not in context_def or context_def['version'] != 1:
                    raise ValueError('Invalid cowait context version')
                context = context_def.get('cowait', {})

        # context root path is the yml folder
        root_path = os.path.abspath(os.path.dirname(context_file_path))

        return CowaitContext(
            root_path=root_path,
            definition=context,
        )
