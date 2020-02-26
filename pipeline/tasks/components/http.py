from aiohttp import web


class HttpComponent():
    def __init__(self, task, port):
        self.port = port
        self.app = web.Application()
        self.add_routes = self.app.router.add_routes
        self.add_route = self.app.router.add_route
        self.add_post = self.app.router.add_post
        self.add_get = self.app.router.add_get

        task.node.io.create_task(self.__serve())

    async def __serve(self):
        runner = web.AppRunner(self.app, handle_signals=False)
        await runner.setup()
        site = web.TCPSite(runner, host='*', port=self.port)
        await site.start()
