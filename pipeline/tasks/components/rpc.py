import inspect
import traceback
from aiohttp import web
from .http import HttpComponent


class RpcComponent():
    def __init__(self, task):
        self.methods = get_rpc_methods(task)
        task.node.children.on('rpc', self.on_rpc)

        # if the task has an http server, automatically add rpc routes
        # fixme: perhaps Task.has_component() or similar?
        if hasattr(task, 'http') and isinstance(task.http, HttpComponent):
            self.add_http_routes(task.http)

    def add_http_routes(self, http):
        for name, func in self.methods.items():
            http.add_post(f'/rpc/{name}', wrap_http_rpc(func))

        # fixme: need a catch-all handler that returns an error
        # currently undefined methods return 404

    async def on_rpc(self, conn, method, args, nonce):
        try:
            if method not in self.methods:
                raise RpcError(f'No such method {method}')

            rpc_func = self.methods[method]
            result = await rpc_func(**args)
            if result is None:
                result = {}

            await conn.send({
                'type': 'rpc_result',
                'nonce': nonce,
                'method': method,
                'args': args,
                'result': result,
            })

        except Exception as e:
            traceback.print_exc()
            await conn.send({
                'type': 'rpc_error',
                'nonce': nonce,
                'method': method,
                'args': args,
                'error': str(e),
            })


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


def wrap_http_rpc(func):
    """ Wraps a function in an HTTP RPC handler """
    async def handler(req):
        try:
            args = await req.json()
            result = await func(**args)
            if result is None:
                result = {}
            return web.json_response(result)
        except Exception as e:
            traceback.print_exc()
            return web.json_response({'error': str(e)}, status=400)

    return handler
