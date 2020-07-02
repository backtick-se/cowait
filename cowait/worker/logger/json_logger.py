import json
from .logger import Logger


class JSONLogger(Logger):
    def log(self, type: str, msg: dict) -> None:
        self.print(json.dumps(msg), flush=True)
