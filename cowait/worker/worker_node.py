import asyncio
from cowait.network import Server, HttpServer, get_local_ip
from cowait.utils import StreamCapturing
from .io_thread import IOThread
from .logger import Logger
from .parent_client import ParentClient


class WorkerNode(object):
    def __init__(self, id: str, upstream: str, port: int = 80, logger: Logger = None):
        super().__init__()
        self.id = id
        self.io = IOThread()
        self.io.start()
        self.upstream = upstream
        self.http = HttpServer(port=port)
        self.children = Server(self)
        self.parent = ParentClient(id, self.io, logger)

    async def connect(self) -> None:
        await self.parent.connect(self.upstream)

    def serve(self):
        self.io.create_task(self.http.serve())

    def get_url(self):
        local_ip = get_local_ip()
        return f'ws://{local_ip}:{self.http.port}/ws'

    async def close(self) -> None:
        async def _close():
            await asyncio.sleep(0.01)
            await self.children.close()
            await self.parent.close()

        await asyncio.sleep(0.01)
        self.io.create_task(_close())

    def capture_logs(self) -> StreamCapturing:
        """ Sets up a stream capturing context, forwarding logs to the node """
        def logger(file):
            def callback(x):
                nonlocal file
                self.io.create_task(self.parent.send_log(file, x))
            return callback

        return StreamCapturing(
            on_stdout=logger('stdout'),
            on_stderr=logger('stderr'),
            silence=True,
        )
