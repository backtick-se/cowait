from cowait.network import Server, HttpServer
from cowait.utils import StreamCapturing
from .io_thread import IOThread
from .parent_client import ParentClient
from .json_logger import JSONLogger


class WorkerNode(object):
    def __init__(self, id, upstream):
        super().__init__()
        self.id = id
        self.io = IOThread()
        self.io.start()
        self.upstream = upstream
        self.http = HttpServer()
        self.children = Server(self)

        if upstream is None:
            self.parent = JSONLogger(id, self.io)
        else:
            self.parent = ParentClient(id, self.io)

    async def connect(self) -> None:
        await self.parent.connect(self.upstream)

    def serve(self):
        self.io.create_task(self.http.serve())

    async def close(self) -> None:
        async def close():
            await self.children.close()
            await self.parent.close()

        self.io.create_task(close())

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
