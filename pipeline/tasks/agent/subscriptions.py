from pipeline.network import Conn
from pipeline.utils import EventEmitter


class Subscriptions(EventEmitter):
    def __init__(self):
        super().__init__()
        self.subscribers = []

    async def forward(self, conn: Conn, **msg):
        if conn in self.subscribers:
            return

        for subscriber in self.subscribers:
            await subscriber.send(msg)

    async def subscribe(self, conn: Conn, **msg):
        print(f'~~ add subscriber {conn.remote_ip}:{conn.remote_port}')
        self.subscribers.append(conn)
        await self.emit(
            type='subscribe',
            conn=conn,
        )

    async def unsubscribe(self, conn: Conn, **msg):
        print(f'~~ drop subscriber {conn.remote_ip}:{conn.remote_port}')
        if conn in self.subscribers:
            self.subscribers.remove(conn)
            await self.emit(
                type='unsubscribe',
                conn=conn,
            )
