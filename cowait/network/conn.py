import aiohttp
from .rpc_client import RpcClient


class Conn(object):
    def __init__(self, ws, remote):
        self.ws = ws
        self.id = None
        self.rpc = RpcClient(ws)
        self.remote = remote

    async def send(self, msg: dict) -> None:
        await self.ws.send_json(msg)

    async def close(self, message=''):
        self.rpc.cancel_all()
        await self.ws.close(
            code=aiohttp.WSCloseCode.GOING_AWAY,
            message=message
        )
