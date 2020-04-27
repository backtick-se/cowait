import aiohttp
from cowait.utils import EventEmitter


class Client(EventEmitter):
    def __init__(self):
        super().__init__()
        self.ws = None

    @property
    def connected(self) -> bool:
        return self.ws is not None

    async def connect(self, url: str, token: str) -> None:
        headers = {
            'Authorization': f'Bearer {token}',
        }
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url, headers=headers) as ws:
                self.ws = ws

                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        event = msg.json()
                        await self.emit(**event, conn=self)
                    elif msg.type == aiohttp.WSMsgType.CLOSE:
                        print('parent ws clean close')
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        print('parent ws client error:', ws.exception())

        self.ws = None

    async def close(self):
        if self.connected:
            await self.ws.close()
            self.ws = None

    async def send(self, msg: dict) -> None:
        if not self.connected:
            raise RuntimeError('Not connected')

        await self.ws.send_json(msg)
