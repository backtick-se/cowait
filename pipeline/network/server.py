import json
import websockets
from .conn import Conn

ANY_IP = '0.0.0.0'


class Server:
    def __init__(self, port: int):
        self.ws = None
        self.port = port
        self.conns = []

    async def serve(self, handler: callable) -> None:
        async def handle(ws, path):
            await self.on_client(ws, handler)

        # serve websockets
        self.ws = await websockets.serve(
            handle,
            host=ANY_IP,
            port=self.port,
        )
        await self.ws.wait_closed()

    async def on_client(self, ws, handler: callable) -> None:
        conn = Conn(ws)
        self.conns.append(conn)

        try:
            while True:
                msg = await conn.recv()
                if msg is None:
                    break

                await handler(conn, msg)

        except websockets.exceptions.ConnectionClosedOK:
            pass

        finally:
            self.conns.remove(conn)

    async def send(self, msg: dict) -> None:
        if self.ws is None:
            raise RuntimeError('call serve() first')

        try:
            js = json.dumps(msg)
            for conn in self.conns:
                await conn.ws.send(js)

        except websockets.exceptions.ConnectionClosedOK:
            return

    def close(self) -> None:
        if self.ws is None:
            return

        self.ws.close()
