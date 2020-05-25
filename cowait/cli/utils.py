import os
from signal import signal, SIGINT
from .const import CONTEXT_FILE_NAME

HEADER_WIDTH = 80

try:
    rows, columns = os.popen('stty size', 'r').read().split()
    HEADER_WIDTH = int(columns)
except Exception:
    pass


class ExitTrap():
    def __init__(self, callback: callable, single=True):
        self.callback = callback
        self.prev_handler = None
        self.single = single

    def __enter__(self):
        self.attach(self.callback)

    def __exit__(self, *exc):
        self.reset()

    def attach(self, callback):
        def handler(a, b):
            if self.single:
                self.reset()
            callback()

        self.reset()
        old = signal(SIGINT, handler)
        self.prev_handler = old

    def reset(self):
        if self.prev_handler is not None:
            signal(SIGINT, self.prev_handler)
            self.prev_handler = None


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


def printheader(title: str = None) -> None:
    if title is None:
        print(f'--'.ljust(HEADER_WIDTH, '-'))
    else:
        print(f'-- {title} '.upper().ljust(HEADER_WIDTH, '-'))
