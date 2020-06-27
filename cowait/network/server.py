import aiohttp
from aiohttp import web
from cowait.utils import EventEmitter
from .conn import Conn


class Server(EventEmitter):
    def __init__(self, node):
        super().__init__()
        self.conns = []
        node.http.add_get('/ws', self.handle_client)

    async def handle_client(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        conn = Conn(ws, request.remote)
        await self.emit(type='__connect', conn=conn)
        self.conns.append(conn)

        try:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    event = msg.json()

                    if conn.rpc.intercept_event(**event):
                        continue

                    await self.emit(**event, conn=conn)

        except Exception as e:
            await self.emit(type='__error', conn=conn, error=str(type(e)))

        finally:
            # disconnected
            self.conns.remove(conn)
            await self.emit(type='__close', conn=conn)

    async def send(self, msg: dict) -> None:
        for ws in self.conns:
            await ws.send_json(msg)

    async def close(self):
        for conn in self.conns:
            await conn.close()
