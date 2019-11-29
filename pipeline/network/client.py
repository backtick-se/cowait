import json
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed


class Client:
    def __init__(self, uri):
        self.ws = None
        self.uri = uri

    async def connect(self, retries: int = 10, delay: float = 1.0):
        # retry loop
        retries_left = retries
        while retries_left > 0 or retries == -1:
            try:
                # attempt to connect
                self.ws = await websockets.connect(self.uri)

                # connection ok, break the loop.
                return

            except (ConnectionRefusedError, ConnectionClosed):
                # wait before next loop
                await asyncio.sleep(delay)

                retries_left -= 1
                delay *= 1.5  # exponential backoff

        # no attempts left - raise error
        raise ConnectionError(
            f'Unable to connect to upstream at {self.uri}'
            f'after {retries} attempts')

    async def send(self, msg: dict) -> None:
        try:
            await self.ws.send(json.dumps(msg))
        except ConnectionClosed:
            pass

    async def recv(self):
        raise NotImplementedError('downstream recv not yet supported')

    async def close(self):
        if self.ws is None:
            return

        return await self.ws.close()
