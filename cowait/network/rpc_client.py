import asyncio
from cowait.types import deserialize
from concurrent.futures import Future
from cowait.tasks.components.rpc import RpcError, \
    RPC_CALL, RPC_ERROR, RPC_RESULT


class RpcCall(Future):
    def __init__(self, method, args, nonce):
        super().__init__()
        self.method = method
        self.args = args
        self.nonce = nonce


class RpcClient(object):
    def __init__(self, ws):
        self.ws = ws
        self.nonce = 0
        self.calls = {}

    async def call(self, method, args):
        nonce = self.nonce
        self.nonce += 1

        self.calls[nonce] = RpcCall(method, args, nonce)
        await self.ws.send_json({
            'type':   RPC_CALL,
            'method': method,
            'args':   args,
            'nonce':  nonce,
        })

        return await asyncio.wrap_future(self.calls[nonce])

    def cancel_all(self):
        for nonce, future in self.calls.items():
            if not future.done():
                future.set_exception(RpcError('Cancelled'))

    def intercept_event(self, type, **msg):
        if type == RPC_RESULT:
            self._rpc_result(**msg)
            return True

        if type == RPC_ERROR:
            self._rpc_error(**msg)
            return True

        return False

    def _rpc_result(self, nonce, result, result_type, **msg):
        result = deserialize(result, result_type)
        future = self.calls[nonce]
        if not future.done():
            future.set_result(result)
        del self.calls[nonce]

    def _rpc_error(self, nonce, error, **msg):
        future = self.calls[nonce]
        if not future.done():
            future.set_exception(RpcError(error))
        del self.calls[nonce]
