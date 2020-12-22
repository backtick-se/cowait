import asyncio
from cowait.network import Server, get_local_ip, WS_PATH
from cowait.utils import StreamCapturing
from .io_thread import IOThread
from .logger import Logger
from .parent_client import ParentClient
from .resource_monitor import ResourceMonitor


class WorkerNode(object):
    def __init__(self, id: str, upstream: str, port: int = 80, logger: Logger = None):
        super().__init__()
        self.id = id
        self.io = IOThread()
        self.io.start()
        self.upstream = upstream
        self.server = Server(port=port)
        self.parent = ParentClient(id, self.io, logger)

    async def connect(self) -> None:
        await self.parent.connect(self.upstream)

    def serve(self):
        self.io.create_task(self.server.serve())

    def get_url(self):
        local_ip = get_local_ip()
        return f'ws://{local_ip}:{self.server.port}/{WS_PATH}'

    async def close(self) -> None:
        async def _close():
            await asyncio.sleep(0.01)
            await self.server.close()
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

    def monitor_system(self, interval: float = 1.0):
        async def monitor_loop():
            monitor = ResourceMonitor()
            while True:
                await asyncio.sleep(interval)
                await self.parent.send_stats(monitor.stats())

        self.io.create_task(monitor_loop())
