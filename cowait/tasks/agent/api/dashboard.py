import os.path
from aiohttp import web

DASH_ROOT = '/var/cowait/cloud/build'


class Dashboard(object):
    def routes(self):
        if not self.is_built():
            print('~~ notice: dashboard not included in build')
            return []

        return [
            web.static('/static/', f'{DASH_ROOT}/static'),
            web.get('/{tail:.*}', self.get_dashboard),
        ]

    def get_dashboard(self, req):
        return web.FileResponse(f'{DASH_ROOT}/index.html')

    @staticmethod
    def is_built():
        return os.path.exists(DASH_ROOT)
