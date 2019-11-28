import os
import yaml
import docker
from .utils import find_file_in_parents
from .const import CONTEXT_FILE_NAME

client = docker.from_env()


class PipelineContext(object):
    def __init__(self, path: str, config: dict):
        self.path = path
        self.config = config

    def __getitem__(self, key):
        return self.config.get(key)

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
        return os.path.relpath(abs_path, self.root)

    @staticmethod
    def open(root_path: str = None):
        if not root_path:
            root_path = os.getcwd()

        # find context file
        context_file_path = find_file_in_parents(root_path, CONTEXT_FILE_NAME)
        if context_file_path is None:
            raise RuntimeError(
                f'Could not find {CONTEXT_FILE_NAME} '
                f'in {root_path} or any of its parent directories.')

        # load yaml
        with open(context_file_path, 'r') as context_file:
            context_def = yaml.load(context_file, Loader=yaml.FullLoader)
            if 'version' not in context_def or context_def['version'] != 1:
                raise RuntimeError('Invalid pipeline context version')

            config = context_def.get('pipeline', {})

        # context path is the enclosing folder
        root_path = os.path.dirname(context_file_path)

        return PipelineContext(
            path=root_path,
            config=config,
        )
