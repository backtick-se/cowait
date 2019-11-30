from pipeline.utils import uuid
from .client import Client
from .server import Server


class Node(object):
    """
    Tree network node.
    """

    def __init__(self):
        self.id = 'node-%s' % uuid(8)
        self.upstream = None
        self.daemon = None
        self.handlers = []

    async def connect(self, uri) -> None:
        self.upstream = Client(uri)
        await self.upstream.connect()

    def bind(self, port) -> None:
        self.daemon = Server(port)

    async def serve(self) -> None:
        async def handle(conn, msg):
            # received upstream message
            for handler in self.handlers:
                if not handler.handle(**msg):
                    return

        await self.daemon.serve(handle)

    async def close(self) -> None:
        if self.daemon:
            self.daemon.close()
        if self.upstream:
            await self.upstream.close()

    async def send(self, msg: dict) -> None:
        """
        Send a message upstream. Also executed by handlers (?)
        """

        for handler in self.handlers:
            if not handler.handle(**msg):
                return

        if self.upstream:
            await self.upstream.send(msg)

    def attach(self, handler: callable) -> None:
        self.handlers.insert(0, handler)

    def detach(self, handler: callable) -> None:
        self.handlers.remove(handler)
