from aiohttp import web
from .auth_middleware import AuthMiddleware


class HttpServer():
    def __init__(self, port: int = 80):
        self.port = port
        self.auth = AuthMiddleware()

        # create http app
        self.app = web.Application(
            middlewares=[self.auth.middleware],
        )

        # route shortcuts
        self.add_routes = self.app.router.add_routes
        self.add_route = self.app.router.add_route
        self.add_post = self.app.router.add_post
        self.add_get = self.app.router.add_get

    async def serve(self):
        runner = web.AppRunner(self.app, handle_signals=False)
        await runner.setup()
        site = web.TCPSite(runner, host='*', port=self.port)
        await site.start()
