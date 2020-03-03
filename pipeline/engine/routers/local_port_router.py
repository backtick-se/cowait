import random
from .router import Router


class LocalPortRouter(Router):
    def __init__(self, cluster):
        super().__init__(cluster)
        cluster.on('prepare', self.on_prepare)

    def on_prepare(self, taskdef):
        for path, port in taskdef.routes.items():
            if path != '/':
                print(f'!! warning: http subdirectory path {path} '
                      'is not routable locally')
                continue

            host_port = random.randint(60000, 65000)
            url = f'http://localhost:{host_port}/'

            # assign route url
            taskdef.routes[path] = {
                'port': port,
                'path': path,
                'url': url,
            }

            # open host port
            taskdef.ports[port] = host_port

            print('~~ http route', path, '->', url)

        return taskdef
