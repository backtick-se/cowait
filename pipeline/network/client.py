import json
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK
from pipeline.utils import EventEmitter


class Client(EventEmitter):
    def __init__(self):
        super().__init__()
        self.ws = None
        self.callbacks

    async def connect(self, uri, retries: int = 10, delay: float = 1.0):
        # retry loop
        retries_left = retries
        while retries_left > 0 or retries == -1:
            try:
                # attempt to connect
                self.ws = await websockets.connect(uri)

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
            pass

    async def recv(self):
        if self.ws is None:
            raise RuntimeError('Not connected')
        try:
            msg = await self.ws.recv()
            return json.loads(msg)

        except ConnectionClosedOK:
            return None

    async def serve(self):
        while True:
            event = await self.recv()
            if event is None:
                return
            await self.emit(**event)

    async def close(self):
        if self.ws is None:
            return

        return await self.ws.close()
