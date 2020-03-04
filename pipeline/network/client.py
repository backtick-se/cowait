import os
import json
import asyncio
import websockets
import traceback
from websockets.exceptions import ConnectionClosed
from pipeline.utils import EventEmitter
from .rpc_client import RpcClient


class Client(EventEmitter):
    def __init__(self):
        super().__init__()
        self.ws = None

    async def connect(self, uri, retries: int = 10, delay: float = 1.0):
        # retry loop
        retries_left = retries
        while retries_left > 0 or retries == -1:
            try:
                # attempt to connect
                self.ws = await websockets.connect(uri)
                self.rpc = RpcClient(self.ws)

                # connection ok, break the loop.
                return

            except (ConnectionRefusedError, ConnectionClosed):
                # wait before next loop
                await asyncio.sleep(delay)

                retries_left -= 1
                delay *= 1.5  # exponential backoff

        # no attempts left - raise error
        raise ConnectionError(
            f'Unable to connect to upstream at {uri}'
            f'after {retries} attempts')

    async def send(self, msg: dict) -> None:
        if self.ws is None:
            raise RuntimeError('Not connected')

        try:
            await self.ws.send(json.dumps(msg))
        except ConnectionClosed:
            print('~~ lost upstream connection!')
            os._exit(1)

    async def recv(self):
        if self.ws is None:
            raise RuntimeError('Not connected')

        try:
            msg = await self.ws.recv()
            return json.loads(msg)

        except ConnectionClosed:
            print('~~ lost upstream connection!')
            os._exit(1)

        except Exception as e:
            await self.close()
            raise e

    async def serve(self, upstream):
        try:
            await self.connect(upstream)
            while True:
                event = await self.recv()
                if event is None:
                    return

                if 'type' not in event:
                    raise RuntimeError('Invalid message', event)

                # intercept RPC communication
                if self.rpc.intercept_msg(event):
                    continue

                await self.emit(**event, conn=self)

        except ConnectionClosed:
            print('~~ lost upstream connection!')
            os._exit(1)

        except Exception:
            print('~~ upstream client exception:')
            traceback.print_exc()
            os._exit(1)

    async def close(self):
        if self.ws is None:
            return

        self.rpc.cancel_all()

        try:
            return await self.ws.close(reason='{}')
        except Exception:
            pass
