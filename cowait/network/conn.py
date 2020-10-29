from aiohttp import WSCloseCode
from datetime import datetime
from .rpc_client import RpcClient


class Conn(object):
    def __init__(self, ws, remote):
        self.ws = ws
        self.id = None
        self.rpc = RpcClient(ws)
        self.remote = remote

    async def send(self, msg: dict) -> None:
        msg['ts'] = datetime.now().isoformat()
        if 'type' not in msg:
            raise Exception('Messages must have a type field')

        await self.ws.send_json(msg)

    async def close(self, message=''):
        self.rpc.cancel_all()
        await self.ws.close(
            code=WSCloseCode.GOING_AWAY,
            message=message
        )
