from cowait.tasks.shell import ShellTask
from cowait.engine import env_pack, \
    ENV_TASK_CLUSTER, ENV_TASK_DEFINITION, ENV_GZIP_ENABLED


class NotebookTask(ShellTask):
    async def run(self, **inputs):
        self.node.http.auth.enabled = False

        if '/' in self.routes:
            print('Notebook available at:')
            print(self.routes['/']['url'])

        await super().run(
            command='jupyter lab',
            env={
                ENV_GZIP_ENABLED: '1',
                ENV_TASK_DEFINITION: env_pack(self.serialize()),
                ENV_TASK_CLUSTER: env_pack(self.cluster.serialize()),
            },
        )

    def filter_stdout(self, line):
        return False

    def filter_stderr(self, line):
        return False
