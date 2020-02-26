import traceback
from aiohttp import web
from .rpc import RpcComponent


class HttpComponent():
    def __init__(self, task, port: int = 80):
        self.task = task
        self.port = port
        self.app = web.Application()
        self.add_routes = self.app.router.add_routes
        self.add_route = self.app.router.add_route
        self.add_post = self.app.router.add_post
        self.add_get = self.app.router.add_get

    def start(self):
        self.__register_rpc_routes()

        # has to be called AFTER all routes are registered
        self.task.node.io.create_task(self.__serve())

    async def __serve(self):
        runner = web.AppRunner(self.app, handle_signals=False)
        await runner.setup()
        site = web.TCPSite(runner, host='*', port=self.port)
        await site.start()

    def __add_rpc_routes(self):
        if hasattr(self.task, 'rpc') and isinstance(self.task, RpcComponent):
            for name, func in self.task.rpc.methods.items():
                self.add_post(f'/rpc/{name}', wrap_http_rpc(func))

        # fixme: need a catch-all handler that returns an error
        # currently undefined methods return 404


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
