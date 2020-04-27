from aiohttp import web
from cowait.utils import uuid


class AuthMiddleware(object):
    def __init__(self):
        self.tokens = {}

    def add_token(self, token: str) -> None:
        self.tokens[token] = True

    def get_token(self) -> str:
        token = uuid(32)
        self.tokens[token] = True
        return token

    def ban_token(self, token: str) -> None:
        self.tokens[token] = False

    def validate_token(self, token: str) -> bool:
        return self.tokens.get(token, False)

    def is_public(self, path):
        if path == '/ws':
            return False
        if path.startswith('/api/'):
            return False
        if path.startswith('/rpc/'):
            return False

        return True

    @web.middleware
    async def middleware(self, request, handler):
        # allow public routes
        if self.is_public(request.path):
            return await handler(request)

        # check for authorization header
        if 'authorization' in request.headers:
            # validate authorization header
            auth = request.headers.get('authorization')
            if 'bearer ' not in auth.lower():
                raise web.HTTPBadRequest(reason='Invalid authorization header')

            token = auth[len('bearer '):]
            if self.validate_token(token):
                return await handler(request)

        # check for query token
        if 'token' in request.query:
            token = request.query['token']
            if self.validate_token(token):
                return await handler(request)

        raise web.HTTPUnauthorized()
