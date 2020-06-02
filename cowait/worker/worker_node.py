import asyncio
from cowait.network import Server, HttpServer
from cowait.utils import StreamCapturing
from .io_thread import IOThread
from .parent_client import ParentClient


class WorkerNode(object):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.io = IOThread()
        self.io.start()

        self.http = HttpServer()
        self.children = Server(self)
        self.parent = ParentClient(id)

    async def connect(self, uri) -> None:
        self.io.create_task(self.parent.connect(uri))
        while not self.parent.connected:
            await asyncio.sleep(0.1)

    async def close(self) -> None:
        async def close():
            if self.children:
                await self.children.close()
            if self.parent:
                await self.parent.close()

        self.io.create_task(close())

    def capture_logs(self) -> StreamCapturing:
        """ Sets up a stream capturing context, forwarding logs to the node """
        def logger(file):
            def callback(x):
                nonlocal file
                self.io.create_task(self.parent.send_log(file, x))
            return callback

        return StreamCapturing(logger('stdout'), logger('stderr'))
