from pipeline.utils import EventEmitter


class NopLogger(EventEmitter):
    def __init__(self):
        super().__init__()
        self.ws = None  # hack due to stdout loop

    async def close(self) -> None:
        pass

    async def recv(self, *args, **kwargs) -> None:
        pass

    async def send(self, msg: dict) -> None:
        await self.emit(**msg)

    async def on_init(self, task: dict, **msg):
        pass

    async def on_status(self, id, status, **msg):
        pass

    async def on_fail(self, id, error, **msg):
        pass

    async def on_return(self, id, result, **msg):
        pass

    async def on_log(self, id, file, data, **msg):
        pass
