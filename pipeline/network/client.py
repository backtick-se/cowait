import json
import asyncio
import websockets
import traceback
from concurrent.futures import Future
from websockets.exceptions import ConnectionClosed, \
    ConnectionClosedOK, ConnectionClosedError
from pipeline.utils import EventEmitter
from pipeline.tasks.components.rpc import RpcError, \
    RPC_CALL, RPC_ERROR, RPC_RESULT


class Client(EventEmitter):
    def __init__(self):
        super().__init__()
        self.ws = None
        self.callbacks
        self.nonce = 0
        self.calls = {}

    async def connect(self, uri, retries: int = 10, delay: float = 1.0):
        # retry loop
        retries_left = retries
        while retries_left > 0 or retries == -1:
            try:
                # attempt to connect
                self.ws = await websockets.connect(uri)

                # connection ok, break the loop.
                return

            except (ConnectionRefusedError, ConnectionClosed):
                # wait before next loop
                await asyncio.sleep(delay)

                retries_left -= 1
                delay *= 1.5  # exponential backoff

        # no attempts left - raise error
        raise ConnectionError(
            f'Unable to connect to upstream at {uri}'
            f'after {retries} attempts')

    async def send(self, msg: dict) -> None:
        if self.ws is None:
            raise RuntimeError('Not connected')
        try:
            await self.ws.send(json.dumps(msg))

        except Exception as e:
            await self.close()
            raise e

        except ConnectionClosed:
            pass

    async def recv(self):
        if self.ws is None:
            raise RuntimeError('Not connected')
        try:
            msg = await self.ws.recv()
            return json.loads(msg)

        except Exception as e:
            await self.close()
            raise e

        except ConnectionClosedOK:
            return None

    async def serve(self, upstream):
        try:
            await self.connect(upstream)
            while True:
                event = await self.recv()
                if event is None:
                    return

                if 'type' not in event:
                    raise RuntimeError('Invalid message', event)

                # intercept RPC results
                if event['type'] == RPC_RESULT:
                    self._rpc_result(**event)
                    continue

                # intercept RPC errors
                if event['type'] == RPC_ERROR:
                    self._rpc_error(**event)
                    continue

                await self.emit(**event, conn=self)

        except (ConnectionClosed, ConnectionClosedError):
            await self.close()

        except Exception as e:
            await self.close()
            traceback.print_exc()
            raise e

    async def close(self):
        for nonce, future in self.calls.items():
            if not future.done():
                future.set_exception(ConnectionClosed(1000, ''))

        if self.ws is None:
            return

        try:
            return await self.ws.close()
        except Exception:
            pass

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
