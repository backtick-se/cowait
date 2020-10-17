import aiohttp
from asyncio import CancelledError
from aiohttp import web
from cowait.utils import EventEmitter
from aiohttp_middlewares import cors_middleware
from .conn import Conn
from .auth_middleware import AuthMiddleware


class Server(EventEmitter):
    def __init__(self, port, middlewares: list = []):
        super().__init__()
        self.conns = []
        self.port = port
        self.auth = AuthMiddleware()

        # create http app
        self.app = web.Application(
            middlewares=[
                *middlewares,
                cors_middleware(allow_all=True)
            ],
        )

        # route shortcuts
        self.add_routes = self.app.router.add_routes
        self.add_route = self.app.router.add_route
        self.add_post = self.app.router.add_post
        self.add_get = self.app.router.add_get

        self.add_get('/ws', self.handle_client)

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

        except CancelledError as e:
            raise e

        except Exception as e:
            await self.emit(type='__error', conn=conn, error=str(type(e)))

        finally:
            # disconnected
            self.conns.remove(conn)
            await self.emit(type='__close', conn=conn)

    async def send(self, msg: dict) -> None:
        for ws in self.conns:
            await ws.send_json(msg)

    async def serve(self):
        self._runner = web.AppRunner(self.app, handle_signals=False)
        await self._runner.setup()

        site = web.TCPSite(self._runner, host='0.0.0.0', port=self.port)
        await site.start()

    async def close(self):
        for conn in self.conns:
            await conn.close()

        await self._runner.cleanup()
        self._runner = None
