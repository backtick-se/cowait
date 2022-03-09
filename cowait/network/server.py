from asyncio import CancelledError
from aiohttp import web, WSMsgType
from aiohttp.helpers import call_later
from aiohttp_middlewares import cors_middleware
from datetime import datetime
from cowait.utils import EventEmitter
from .conn import Conn
from .const import WS_PATH, ON_CONNECT, ON_CLOSE, ON_ERROR
from .auth_middleware import AuthMiddleware
from .errors import SocketError


class FixedWebSocketResponse(web.WebSocketResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _ping(self):
        try:
            await self._writer.ping()
        except ConnectionResetError:
            pass

    def _send_heartbeat(self) -> None:
        if self._heartbeat is not None and not self._closed:
            assert self._loop is not None
            self._loop.create_task(self._ping())  # type: ignore[union-attr]

            if self._pong_response_cb is not None:
                self._pong_response_cb.cancel()
            self._pong_response_cb = call_later(
                self._pong_not_received, self._pong_heartbeat, self._loop
            )


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
                self.auth.middleware,
                cors_middleware(allow_all=True)
            ],
        )

        # route shortcuts
        self.add_routes = self.app.router.add_routes
        self.add_route = self.app.router.add_route
        self.add_post = self.app.router.add_post
        self.add_get = self.app.router.add_get

        self.add_get(f'/{WS_PATH}', self.handle_client)

    async def handle_client(self, request):
        ws = FixedWebSocketResponse(
            timeout=30.0,
            autoping=True,
            heartbeat=5.0,
        )
        await ws.prepare(request)

        conn = Conn(ws, request.remote)
        await self.emit(type=ON_CONNECT, conn=conn)
        self.conns.append(conn)

        try:
            while not ws.closed:
                msg = await ws.receive()
                if msg.type == WSMsgType.CLOSE:
                    break
                elif msg.type == WSMsgType.ERROR:
                    raise SocketError(ws.exception())
                elif msg.type == WSMsgType.BINARY:
                    raise SocketError('Unexpected binary message')
                elif msg.type == WSMsgType.TEXT:
                    event = msg.json()
                    if conn.rpc.intercept_event(**event):
                        continue
                    await self.emit(**event, conn=conn)

            await self.emit(type=ON_CLOSE, conn=conn)

        except CancelledError:
            await self.emit(type=ON_CLOSE, conn=conn)

        except SocketError as e:
            await self.emit(type=ON_CLOSE, conn=conn, error=str(e))

        finally:
            # disconnected
            self.conns.remove(conn)

    async def send(self, msg: dict) -> None:
        msg['ts'] = datetime.now().isoformat()
        if 'type' not in msg:
            raise Exception('Messages must have a type field')

        for ws in self.conns:
            await ws.send_json(msg)

    async def serve(self) -> None:
        self._runner = web.AppRunner(self.app, handle_signals=False)
        await self._runner.setup()

        site = web.TCPSite(self._runner, host='0.0.0.0', port=self.port)
        await site.start()

    async def close(self) -> None:
        for conn in self.conns:
            await conn.close()

        await self._runner.cleanup()
        self._runner = None
