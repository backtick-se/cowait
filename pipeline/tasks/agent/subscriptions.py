from pipeline.network import Conn
from pipeline.utils import EventEmitter
from websockets.exceptions import ConnectionClosedError


class Subscriptions(EventEmitter):
    """ Websocket subscriber component """

    def __init__(self, task):
        super().__init__()
        self.subscribers = []

        task.node.children.on('subscribe', self.subscribe)
        task.node.children.on('unsubscribe', self.unsubscribe)
        task.node.children.on('__close', self.unsubscribe)
        task.node.children.on('*', self.forward)

    async def forward(self, conn: Conn, **msg):
        if conn in self.subscribers:
            return

        for subscriber in self.subscribers:
            try:
                await subscriber.send(msg)
            except ConnectionClosedError:
                pass

    async def subscribe(self, conn: Conn, **msg):
        print(f'~~ add subscriber {conn.remote_ip}:{conn.remote_port}')
        self.subscribers.append(conn)
        await self.emit(
            type='subscribe',
            conn=conn,
        )

    async def unsubscribe(self, conn: Conn, **msg):
        if conn in self.subscribers:
            print(f'~~ drop subscriber {conn.remote_ip}:{conn.remote_port}')
            self.subscribers.remove(conn)
            await self.emit(
                type='unsubscribe',
                conn=conn,
            )
        else:
            print(f'~~ drop task {conn.remote_ip}:{conn.remote_port}')
