import os
from .const import CONTEXT_FILE_NAME


def find_file_in_parents(start_path, file_name):
    """ Finds a file in a directory or any of its parent directories. """

    if not os.path.isdir(start_path):
        raise FileNotFoundError(f'Start directory not found at {start_path}')

    check_path = start_path
    while True:
        files = os.listdir(check_path)

        # if the file is found within the current directory, return its path
        if file_name in files:
            return os.path.join(check_path, file_name)

        # we have reached the root of the task context
        # if the file is not found by now - it doesn't exist
        if CONTEXT_FILE_NAME in files:
            return None

        # reached the file system root, abort mission
        # this will happen when the tool is run outside a task context
        if check_path == '/':
            return None

        # goto parent directory and keep looking
        check_path = os.path.dirname(check_path)