import json
import asyncio
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK
from concurrent.futures import Future
from pipeline.tasks.components.rpc import RpcError, \
    RPC_CALL, RPC_ERROR, RPC_RESULT


class Conn:
    """
    Represents a client->server connection.
    """

    def __init__(self, ws):
        self.ws = ws
        self.id = None
        self.nonce = 0
        self.calls = {}

    async def recv(self):
        try:
            js = await self.ws.recv()
            msg = json.loads(js)

            if 'type' not in msg:
                raise RuntimeError(f'Invalid message: {js}')

            # intercept RPC results
            if msg['type'] == RPC_RESULT:
                self._rpc_result(**msg)
                return await self.recv()

            # intercept RPC errors
            if msg['type'] == RPC_ERROR:
                self._rpc_error(**msg)
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
        for nonce, future in self.calls.items():
            if not future.done():
                future.set_exception(ConnectionClosed(1000, ''))

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

    async def rpc(self, method, args):
        nonce = self.nonce
        self.nonce += 1

        self.calls[nonce] = Future()
        await self.send({
            'type': RPC_CALL,
            'method': method,
            'args': args,
            'nonce': nonce,
        })

        return await asyncio.wrap_future(self.calls[nonce])

    def _rpc_result(self, nonce, result, **msg):
        self.calls[nonce].set_result(result)
        del self.calls[nonce]

    def _rpc_error(self, nonce, error, **msg):
        self.calls[nonce].set_exception(RpcError(error))
        del self.calls[nonce]
