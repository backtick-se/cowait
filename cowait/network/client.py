import os
import asyncio
import aiohttp
from cowait.utils import EventEmitter
from .rpc_client import RpcClient


class AuthError(Exception):
    pass


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
            except aiohttp.ClientError as e:
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
        headers = {'Authorization': f'Bearer {token}'}
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url, headers=headers) as ws:
                self.ws = ws
                self.rpc = RpcClient(ws)
                await self.emit('__connect', conn=self)

                # send buffered messages
                for msg in self.buffer:
                    await self.send(msg)
                self.buffer = []

                # client loop
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        event = msg.json()

                        if self.rpc.intercept_event(**event):
                            continue

                        await self.emit(**event, conn=self)

                    elif msg.type == aiohttp.WSMsgType.CLOSE:
                        break

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        await self.emit('__error', conn=self, error=ws.exception())
                        break

                await self.emit('__close', conn=self)

    async def close(self):
        if self.connected:
            await self.ws.close()
            self.ws = None

    async def send(self, msg: dict) -> None:
        if not self.connected:
            # buffer messages while disconnected
            self.buffer.append(msg)
            return

        await self.ws.send_json(msg)
