import inspect
import traceback
from aiohttp import web
from cowait.types import typed_async_call

RPC_CALL = 'rpc/call'
RPC_ERROR = 'rpc/error'
RPC_RESULT = 'rpc/result'


class RpcComponent():
    def __init__(self, task):
        self.task = task
        self.methods = get_rpc_methods(task)

        # listen for websocket rpc
        task.node.parent.on(RPC_CALL, self.on_rpc)
        task.node.server.on(RPC_CALL, self.on_rpc)

        # register http handler
        task.node.server.add_post('/rpc/{method}', self.http_rpc_handler)

    def get_method(self, method: str) -> callable:
        if method not in self.methods:
            raise RpcError(f'No such method {method}')

        return self.methods[method]

    async def call(self, method, args):
        rpc_func = self.get_method(method)
        result, _ = await typed_async_call(rpc_func, args)
        return result

    async def on_rpc(self, conn, method, args, nonce):
        try:
            rpc_func = self.get_method(method)

            result, result_type = await typed_async_call(rpc_func, args)

            await conn.send({
                'type': RPC_RESULT,
                'id': self.task.id,
                'nonce': nonce,
                'method': method,
                'args': args,
                'result': result,
                'result_type': result_type.describe(),
            })

        except Exception as e:
            traceback.print_exc()
            await conn.send({
                'type': RPC_ERROR,
                'id': self.task.id,
                'nonce': nonce,
                'method': method,
                'args': args,
                'error': str(e),
            })

    async def http_rpc_handler(self, req):
        try:
            call = await req.json()
            args = call.get('args', {})
            method = req.match_info['method']
            result = await self.call(method, args)
            return web.json_response({
                'success': True,
                'result': result,
            })
        except Exception as e:
            print('HTTP RPC Error:')
            traceback.print_exc()
            return web.json_response(
                {
                    'success': False,
                    'error': str(e),
                },
                status=400
            )


class RpcError(RuntimeError):
    pass


def rpc(f):
    """ Decorator for marking RPC methods """
    setattr(f, 'rpc', True)
    return f


def is_rpc_method(object):
    """ Returns true if the given object is a method marked with @rpc """
    if not inspect.ismethod(object):
        return False
    return hasattr(object, 'rpc')


def get_rpc_methods(object):
    """ Returns a dict of functions marked with @rpc on the given object """
    methods = inspect.getmembers(object, is_rpc_method)
    return {name: func for name, func in methods}
