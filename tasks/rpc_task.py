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
    return inspect.getmembers(object, is_rpc_method)


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


class RpcTask(Flow):
    async def before(self, inputs: dict) -> None:
        inputs = await super().before(inputs)
        self.node.children.on('rpc', self.__on_rpc)

        app = web.Application()

        # register rpc methods
        self.rpc = {}
        for name, func in get_rpc_methods(self):
            self.rpc[name] = func
            handler = wrap_http_rpc(func)
            app.router.add_post(f'/rpc/{name}', handler)

        # run web server coroutine on io thread
        self.node.io.create_task(web._run_app(
            app=app,
            port=1338,
            print=False,
            handle_signals=False,
        ))

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

    async def __on_rpc(self, conn, method, args, nonce):
        try:
            if method not in self.rpc:
                raise RpcError(f'No such method {method}')

            rpc_func = self.rpc[method]
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
