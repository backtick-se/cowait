import traceback
from aiohttp import web


class HttpComponent():
    def __init__(self, task, port: int = 80):
        self.task = task
        self.port = port
        self.app = web.Application()
        self.add_routes = self.app.router.add_routes
        self.add_route = self.app.router.add_route
        self.add_post = self.app.router.add_post
        self.add_get = self.app.router.add_get
        self.__add_rpc_route(self.task)

    def start(self):
        """ Start the server. Must be called AFTER routes are registered. """
        self.task.node.io.create_task(self.__serve())

    async def __serve(self):
        runner = web.AppRunner(self.app, handle_signals=False)
        await runner.setup()
        site = web.TCPSite(runner, host='*', port=self.port)
        await site.start()

    def __add_rpc_route(self, task):
        async def rpc_handler(req):
            try:
                args = await req.json()
                method = req.match_info['method']
                result = await task.rpc.call(method, args)
                return web.json_response(result)
            except Exception as e:
                print('HTTP RPC Error:')
                traceback.print_exc()
                return web.json_response({'error': str(e)}, status=400)

        self.add_post('/rpc/{method}', rpc_handler)
