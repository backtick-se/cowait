import os
import asyncio
from datetime import datetime
from aiohttp import WSMsgType, ClientError, ClientSession
from cowait.utils import EventEmitter
from .rpc_client import RpcClient
from .const import ON_CONNECT, ON_CLOSE, ON_ERROR
from .errors import AuthError, SocketError


class Client(EventEmitter):
    def __init__(self):
        super().__init__()
        self.ws = None
        self.rpc = None
        self.buffer = []

    @property
    def connected(self) -> bool:
        return self.ws is not None

    async def connect(
        self,
        url: str,
        token: str,
        max_retries: int = 5
    ) -> None:
        retries = 0
        while retries < max_retries or max_retries == 0:
            retries += 1
            try:
                await self._connect(url, token)
            except ClientError as e:
                if hasattr(e, 'status') and e.status == 401:
                    raise AuthError('Upstream authentication failed')
                else:
                    print('Upstream connection failed:', str(e))
                    await asyncio.sleep(retries * 3)
            finally:
                self.ws = None

        if retries >= max_retries and max_retries > 0:
            # Reached maximum number of connection attempts
            # Crash the client
            print('Max upstream connection attempts reached')
            os._exit(1)

    async def _connect(self, url: str, token: str) -> None:
        async with ClientSession() as session:
            async with session.ws_connect(
                url,
                headers={'Authorization': f'Bearer {token}'},
                autoping=True,
                heartbeat=5.0,
                timeout=30.0,
            ) as ws:
                self.ws = ws
                self.rpc = RpcClient(ws)
                await self.emit(ON_CONNECT, conn=self)

                # send buffered messages
                for msg in self.buffer:
                    await self.send(msg)
                self.buffer = []

                # client loop
                try:
                    while not ws.closed:
                        msg = await ws.receive()
                        if msg.type == WSMsgType.CLOSING:
                            break
                        elif msg.type == WSMsgType.ERROR:
                            raise SocketError(ws.exception())
                        elif msg.type == WSMsgType.BINARY:
                            raise SocketError('Unexpected binary message')

                        event = msg.json()
                        if self.rpc.intercept_event(**event):
                            continue
                        await self.emit(**event, conn=self)

                    await self.emit(ON_CLOSE, conn=self)

                except SocketError as e:
                    await self.emit(ON_ERROR, conn=self, error=str(e))

                finally:
                    self.ws = None

    async def close(self):
        if self.connected:
            await self.ws.close()
        self.ws = None

    async def send(self, msg: dict) -> None:
        msg['ts'] = datetime.now().isoformat()
        if 'type' not in msg:
            raise Exception('Messages must have a type field')

        if not self.connected:
            # buffer messages while disconnected
            self.buffer.append(msg)
            return

        await self.ws.send_json(msg)
