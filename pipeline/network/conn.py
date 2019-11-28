import json
from websockets.exceptions import ConnectionClosedOK


class Conn:
    """
    Represents a server->client connection.
    """

    def __init__(self, ws):
        self.ws = ws

    async def recv(self):
        try:
            js = await self.ws.recv()
            return json.loads(js)

        except ConnectionClosedOK:
            return None

    async def send(self, msg: dict) -> None:
        try:
            js = json.dumps(msg)
            await self.ws.send(js)

        except ConnectionClosedOK:
            pass
