import json
import websockets


class Client:
    def __init__(self, uri):
        self.uri = uri


    async def connect(self):
        self.ws = await websockets.connect(self.uri)


    async def send(self, msg):
        await self.ws.send(json.dumps(msg))
    

    async def close(self):
        return await self.ws.close()
