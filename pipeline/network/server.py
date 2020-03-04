import aiohttp
from aiohttp import web
from pipeline.utils import EventEmitter
from .conn import Conn


class Server(EventEmitter):
    def __init__(self, port):
        super().__init__()
        self.conns = []
        self.port = port

    async def handle_client(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        conn = Conn(ws, request.remote)
        self.conns.append(conn)

        await self.emit(type='__connect', conn=conn)

        # connected!
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                event = msg.json()

                if conn.rpc.intercept_event(event):
                    continue

                await self.emit(**event, conn=conn)

            elif msg.type == aiohttp.WSMsgType.CLOSE:
                print('ws clean exit')

            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws error', ws.exception())

        # disconnected
        self.conns.remove(conn)
        await self.emit(type='__close', conn=conn)

    async def send(self, msg: dict) -> None:
        for ws in self.conns:
            await ws.send_json(msg)

    async def close(self):
        for conn in self.conns:
            await conn.close()

    async def serve(self):
        app = web.Application()
        app.add_routes([
            web.get('/', self.handle_client)
        ])
        runner = web.AppRunner(app, handle_signals=False)
        await runner.setup()
        site = web.TCPSite(runner, host='*', port=self.port)
        await site.start()
