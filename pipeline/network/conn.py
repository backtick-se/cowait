import json
from websockets.exceptions import ConnectionClosedOK


class Conn:
    """
    Represents a client->server connection.
    """

    def __init__(self, ws):
        self.ws = ws
        self.id = None

    async def recv(self):
        js = await self.ws.recv()
        return json.loads(js)

    async def send(self, msg: dict) -> None:
        try:
            js = json.dumps(msg)
            await self.ws.send(js)

        except ConnectionClosedOK:
            pass

    @property
    def remote_ip(self):
        return self.ws.remote_address[0]

    @property
    def remote_port(self):
        return self.ws.remote_address[1]
