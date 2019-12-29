from pipeline.utils import uuid
from .client import Client
from .server import Server
from .service import NodeService


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

    async def serve_upstream(self) -> None:
        async def handle(conn, msg):
            # received upstream message
            for handler in self.handlers:
                if not handler.handle_upstream(**msg):
                    return

            # pass upstream
            if self.upstream:
                await self.upstream.send(msg)

        await self.daemon.serve(handle)

    async def serve_downstream(self) -> None:
        while True:
            msg = await self.upstream.recv()
            if msg is None:
                return

            print('~~ downstream:', msg)

            # received downstream message
            for handler in self.handlers:
                if not handler.handle_downstream(**msg):
                    return

    async def close(self) -> None:
        if self.daemon:
            self.daemon.close()
        if self.upstream:
            await self.upstream.close()

    async def send_up(self, msg: dict) -> None:
        """
        Send a message upstream. Also executed by handlers (?)
        """
        for handler in self.handlers:
            if not handler.handle_upstream(**msg):
                return

        if self.upstream:
            await self.upstream.send(msg)

    async def send_down(self, msg: dict) -> None:
        pass

    def attach(self, handler: NodeService) -> None:
        self.handlers.insert(0, handler)

    def detach(self, handler: NodeService) -> None:
        self.handlers.remove(handler)
