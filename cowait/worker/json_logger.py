import json
import sys
from .parent_client import ParentClient


class JSONLogger(ParentClient):
    def __init__(self, id, io_thread):
        super().__init__(id, io_thread)
        self.ws = None  # hack due to stdout loop
        self.stdout = sys.stdout

    async def connect(self, url) -> None:
        pass

    async def close(self) -> None:
        pass

    async def send(self, msg: dict) -> None:
        self.io.create_task(self.dump_json(msg))

    async def dump_json(self, msg):
        print(json.dumps(msg), file=self.stdout)
