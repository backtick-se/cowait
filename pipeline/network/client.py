import json
import websockets
from websockets.exceptions import ConnectionClosedOK


class Client:
    def __init__(self, uri):
        self.uri = uri


    async def connect(self):
        try:
            self.ws = await websockets.connect(self.uri)
        except ConnectionClosedOK:
            return None


    async def send(self, msg):
        try:
            await self.ws.send(json.dumps(msg))
        except ConnectionClosedOK:
            return None
    

    async def close(self):
        return await self.ws.close()
