import json
from ..parent_client import ParentClient
from cowait.tasks.messages import \
    TASK_INIT, TASK_STATUS, TASK_FAIL, TASK_RETURN, TASK_LOG

logged_types = [
    TASK_INIT,
    TASK_STATUS,
    TASK_FAIL,
    TASK_RETURN,
    TASK_LOG,
]


class FlowLogger(ParentClient):
    def __init__(self, id: str):
        super().__init__(id)
        self.ws = None  # hack due to stdout loop
        self.on(TASK_INIT, self.on_init)
        self.on(TASK_STATUS, self.on_status)
        self.on(TASK_FAIL, self.on_fail)
        self.on(TASK_RETURN, self.on_return)
        self.on(TASK_LOG, self.on_log)

    async def connect(self, url) -> None:
        pass

    async def close(self) -> None:
        pass

    async def send(self, msg: dict) -> None:
        if msg['type'] in logged_types:
            await self.emit(**msg)

    async def on_init(self, task: dict, **msg):
        print('~~ create', task['id'], 'from', task['image'], task['inputs'])

    async def on_status(self, id, status, **msg):
        print('~~', id, 'changed status to', status)

    async def on_fail(self, id, error, **msg):
        print('~~', id, 'failed with error:')
        print(error.strip())

    async def on_return(self, id, result, **msg):
        print('~~', id, 'returned:', json.dumps(result, indent=2))

    async def on_log(self, id, file, data, **msg):
        print(data, end='')

    async def send_log(self, file: str, data: str) -> None:
        # no need to forward local logs, they will be sent to stdout anyway
        pass
