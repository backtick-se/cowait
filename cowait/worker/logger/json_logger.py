import os
import json
from datetime import datetime
from .logger import Logger


class JSONLogger(Logger):
    def __init__(self):
        # create a duplicate of stdout early on, so that output from the logger
        # won't be captured and cause a infinite recursion
        self.stdout = os.dup(1)

    def __del__(self):
        os.close(self.stdout)

    def log(self, type: str, msg: dict) -> None:
        msg['ts'] = datetime.now().isoformat()
        jsonstr = json.dumps(msg) + '\n'
        os.write(self.stdout, jsonstr.encode('utf-8'))
