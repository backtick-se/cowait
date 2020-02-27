import json
from websockets.exceptions import ConnectionClosedOK
from .rpc_client import RpcClient


class Conn(object):
    """
    Represents a client->server connection.
    """

    def __init__(self, ws):
        self.ws = ws
        self.id = None
        self.rpc = RpcClient(ws)

    async def recv(self):
        try:
            js = await self.ws.recv()
            msg = json.loads(js)

            if 'type' not in msg:
                raise RuntimeError(f'Invalid message: {js}')

            # intercept RPC communication
            if self.rpc.intercept_msg(msg):
                return await self.recv()

            return msg

        except Exception as e:
            await self.close()
            raise e

    async def send(self, msg: dict) -> None:
        try:
            js = json.dumps(msg)
            await self.ws.send(js)

        except Exception as e:
            await self.close()
            raise e

        except ConnectionClosedOK:
            pass

    async def close(self):
        self.rpc.cancel_all()

        try:
            return await self.ws.close()
        except Exception:
            pass

    @property
    def remote_ip(self):
        return self.ws.remote_address[0]

    @property
    def remote_port(self):
        return self.ws.remote_address[1]
