from pipeline.utils import uuid
from .client import Client
from .server import Server
from .utils import PORT


class Node(object):
    """
    Tree network node.
    """

    def __init__(self):
        self.id = 'node-%s' % uuid(8)
        self.parent = Client()
        self.children = Server(PORT)

    async def connect(self, uri) -> None:
        await self.parent.connect(uri)

    async def close(self) -> None:
        if self.children:
            self.children.close()
        if self.parent:
            await self.parent.close()

    def attach(self, service):
        service.attach(self)
