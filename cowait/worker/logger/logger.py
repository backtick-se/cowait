import sys


class Logger(object):
    def __init__(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    async def handle(self, msg: dict) -> None:
        self.log(msg['type'], msg)

    def log(self, type: str, msg: dict) -> None:
        pass

    def print(self, *args, **kwargs) -> None:
        print(*args, file=self.stdout, **kwargs)

    def print_err(self, *args, **kwargs) -> None:
        print(*args, file=self.stderr, **kwargs)
