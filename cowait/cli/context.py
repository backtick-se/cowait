import os
import os.path
from dotenv import dotenv_values
from cowait.utils.const import DEFAULT_BASE_IMAGE
from .utils import find_file_in_parents
from .const import CONTEXT_FILE_NAME
from .config import Config


class Context(Config):
    def __init__(self, root_path: str, *, path: str, parent: Config):
        super().__init__(
            path=path,
            parent=parent,
            data={} if not path else None,
        )
        self.root_path = root_path

    @property
    def workdir(self) -> str:
        return self.get('workdir', '.', False)

    @property
    def image(self):
        return self.get('image', DEFAULT_BASE_IMAGE, False)

    @property
    def base(self):
        return self.get('base', DEFAULT_BASE_IMAGE, False)

    @property
    def environment(self):
        return {
            **self.get('environment', {}, False),
            **dotenv_values(self.file('.env')),
        }

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

    def pack_data(self, data: dict) -> dict:
        return {
            'version': 1,
            'cowait': data
        }

    def unpack_data(self, data: dict) -> dict:
        if data is None:
            return {}

        if 'version' not in data:
            raise RuntimeError('Invalid context file, no version set.')

        version = int(data['version'])
        if version != 1:
            raise RuntimeError('Wrong context version, expected 1')

        return data.get('cowait', {})

    def write(self, path: str = None) -> None:
        if path is None:
            path = os.path.join(self.root_path, CONTEXT_FILE_NAME)
        return super().write(path)

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
    def open(config: Config, path: str = None):
        if path is None:
            path = os.getcwd()

        # ensure the provided path is an actual directory
        if not os.path.isdir(path):
            raise ValueError(f'Invalid context path {path}: Not a directory')

        # find context root by looking for the context definition file
        context_file_path = find_file_in_parents(path, CONTEXT_FILE_NAME)
        if context_file_path is None:
            # use the current directory as the context
            # no local configuration exists
            return Context(
                root_path=os.path.abspath(path),
                parent=config,
                path=None,
            )

        # context root path is the yml folder
        root_path = os.path.abspath(os.path.dirname(context_file_path))
        return Context(
            root_path=root_path,
            path=context_file_path,
            parent=config,
        )
