import json
import websockets
from pipeline.utils import EventEmitter
from .conn import Conn

ANY_IP = '0.0.0.0'


class Server(EventEmitter):
    def __init__(self, port: int):
        super().__init__()
        self.ws = None
        self.port = port
        self.conns = []

    async def serve(self) -> None:
        self.ws = await websockets.serve(
            self.handle_client,
            host=ANY_IP,
            port=self.port,
        )
        await self.ws.wait_closed()

    async def handle_client(self, ws, path: str) -> None:
        conn = Conn(ws)
        self.conns.append(conn)

        try:
            await self.emit(type='__connect', conn=conn)
            while True:
                msg = await conn.recv()
                if msg is None:
                    break
                await self.emit(**msg, conn=conn)

        except websockets.exceptions.ConnectionClosedOK:
            pass

        finally:
            self.conns.remove(conn)
            await self.emit(type='__close', conn=conn)

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
