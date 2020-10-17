from cowait.network import Conn, ON_CLOSE
from cowait.utils import EventEmitter


class Subscriptions(EventEmitter):
    """ Websocket subscriber component """

    def __init__(self, task):
        super().__init__()
        self.subscribers = []
        self.__len__ = self.subscribers.__len__
        self.__str__ = self.subscribers.__str__
        self.__iter__ = self.subscribers.__iter__
        self.__getitem__ = self.subscribers.__getitem__
        self.__contains__ = self.subscribers.__contains__

        task.node.server.on('subscribe', self.subscribe)
        task.node.server.on('unsubscribe', self.unsubscribe)
        task.node.server.on(ON_CLOSE, self.unsubscribe)
        task.node.server.on('*', self.forward)

    async def forward(self, conn: Conn, **msg):
        if conn in self.subscribers:
            return

        if msg.get('type', '__')[:2] == '__':
            return

        for subscriber in self.subscribers:
            await subscriber.send(msg)

    async def subscribe(self, conn: Conn, **msg):
        print(f'~~ add subscriber {conn.remote}')
        self.subscribers.append(conn)
        await self.emit(
            type='subscribe',
            conn=conn,
        )

    async def unsubscribe(self, conn: Conn, **msg):
        if conn in self.subscribers:
            print(f'~~ drop subscriber {conn.remote}')
            self.subscribers.remove(conn)
            await self.emit(
                type='unsubscribe',
                conn=conn,
            )
        else:
            print(f'~~ drop task {conn.remote}')
