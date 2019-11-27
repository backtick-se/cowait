import asyncio
from typing import Any
from .client import Client
from .server import Server


class Node(object):
    """
    Tree network node.
    """

    def __init__(self, id):
        self.id = id
        self.upstream = None
        self.daemon = None
        self.handlers = [ ]


    async def connect(self, target) -> None:
        self.upstream = Client(target)
        await self.upstream.connect()


    def bind(self, port) -> None:
        self.daemon = Server(port)


    async def serve(self) -> None:
        async def handle(conn, msg):
            # received upstream message
            for handler in self.handlers:
                handler.handle(**msg)

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

        if isinstance(msg, list):
            for m in msg:
                await self.send(m)
        else:
            if not 'id' in msg:
                msg['id'] = self.id

            if self.upstream:
                await self.upstream.send(msg)

            for handler in self.handlers:
                handler.handle(**msg)

    
    def attach(self, handler: callable) -> None:
        self.handlers.append(handler)


    def detach(self, handler: callable) -> None:
        self.handlers.remove(handler)
