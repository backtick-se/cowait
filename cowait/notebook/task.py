import re
from cowait.tasks.shell import ShellTask
from cowait.engine import env_pack, \
    ENV_TASK_CLUSTER, ENV_TASK_DEFINITION, ENV_GZIP_ENABLED
from .kernel import ENV_KERNEL_TOKEN

TOKEN_PATTERN = re.compile('\\?token\\=([a-z0-9]+)')


class NotebookTask(ShellTask):
    def init(self):
        self.jupyter_token = None

    async def run(self, **inputs):
        print('Starting JupyterLab...')

        await super().run(
            command='jupyter lab',
            env={
                ENV_GZIP_ENABLED: '1',
                ENV_TASK_DEFINITION: env_pack(self.taskdef.serialize()),
                ENV_TASK_CLUSTER: env_pack(self.cluster.serialize()),
                ENV_KERNEL_TOKEN: self.node.server.auth.get_token(),
            },
        )

    def on_ready(self):
        print()
        print('JupyterLab ready!')
        if '/' in self.taskdef.routes:
            url = self.taskdef.routes['/']['url']
            print('Notebook available at:')
            print(f'  {url}?token={self.jupyter_token}')
        else:
            print('Warning: No route set')

    def filter_stdout(self, line):
        return self.filter_jupyter_token(line)

    def filter_stderr(self, line):
        return self.filter_jupyter_token(line)

    def filter_jupyter_token(self, line):
        if self.jupyter_token is None:
            match = re.search(TOKEN_PATTERN, line)
            if match is not None:
                self.jupyter_token = match[1]
                self.on_ready()
        return False
