import json
from datetime import datetime
from .logger import Logger


class JSONLogger(Logger):
    def log(self, type: str, msg: dict) -> None:
        msg['ts'] = datetime.now().isoformat()
        self.print(json.dumps(msg), flush=True)
