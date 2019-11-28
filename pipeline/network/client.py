import json
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed


class Client:
    def __init__(self, uri):
        self.ws = None
        self.uri = uri
        self.queue = []

    async def connect(self, retries: int = 3, delay: float = 1.0):
        retries_left = retries
        while retries_left > 0:
            try:
                self.ws = await websockets.connect(self.uri)

                # send message buffer
                for msg in self.queue:
                    await self.ws.send(msg)
                self.queue = []

                # connection ok, break the loop.
                return

            except (ConnectionRefusedError, ConnectionClosed):
                retries_left -= 1
                await asyncio.sleep(delay)

        raise ConnectionError(
            f'Unable to connect to upstream at {self.uri}'
            f'after {retries} attempts')

    async def send(self, msg: dict) -> None:
        data = json.dumps(msg)

        if self.ws is None:
            self.queue.append(data)
            return

        try:
            await self.ws.send(data)
        except ConnectionClosed:
            pass

    async def recv(self):
        raise NotImplementedError('downstream recv not yet supported')

    async def close(self):
        if self.ws is None:
            return

        return await self.ws.close()
