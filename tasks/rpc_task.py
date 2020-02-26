from pipeline.tasks import Flow, sleep

import inspect
import traceback
from aiohttp import web


class RpcError(RuntimeError):
    pass


def rpc(f):
    """ Decorator for marking RPC methods """
    setattr(f, 'rpc', True)
    return f


def is_rpc_method(object):
    if not inspect.ismethod(object):
        return False
    return hasattr(object, 'rpc')


def get_rpc_methods(object):
    methods = inspect.getmembers(object, is_rpc_method)
    return {name: func for name, func in methods}


def wrap_http_rpc(func):
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


class HttpServer():
    def __init__(self, port):
        self.port = port
        self.app = web.Application()
        self.add_routes = self.app.router.add_routes
        self.add_route = self.app.router.add_route
        self.add_post = self.app.router.add_post
        self.add_get = self.app.router.add_get

    async def serve(self):
        runner = web.AppRunner(self.app, handle_signals=False)
        await runner.setup()
        site = web.TCPSite(runner, host='*', port=self.port)
        await site.start()


class RpcComponent():
    def __init__(self, task):
        self.methods = get_rpc_methods(task)
        task.node.children.on('rpc', self.on_rpc)

    def add_http_routes(self, http):
        for name, func in self.methods.items():
            http.add_post(f'/rpc/{name}', wrap_http_rpc(func))

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


class RpcTask(Flow):
    async def before(self, inputs: dict) -> None:
        inputs = await super().before(inputs)

        # run web server coroutine on io thread
        http = HttpServer(port=1338)
        self.node.io.create_task(http.serve())

        # create rpc handler
        self.rpc = RpcComponent(self)
        self.rpc.add_http_routes(http)

        return inputs

    async def run(self, **inputs):
        while True:
            await sleep(1)

    @rpc
    async def rpc_test(self, param):
        print('rpc!', param)
        return param

    @rpc
    async def kill(self):
        print('aborted by rpc')
        await self.stop()
