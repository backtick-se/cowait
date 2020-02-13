from pipeline.tasks.container import ContainerTask

TOKEN_STR = '?token='
TOKEN_LEN = 48


class JupyterTask(ContainerTask):
    async def run(
        self,
        workers: int = 0, worker_cores: int = 2, worker_memory: int = 2,
    ):
        print('Creating jupyter notebook...')
        print(f'Default workers: {workers}')
        print(f'Workers core: {worker_cores}')
        print(f'Worker memory: {worker_memory}')

        await super().run(
            name='jupyter',
            image='docker.backtick.se/dask-notebook:latest',
            routes={
                '/': 8888,
                '/dashboard': 8787,
            },
            cpu=worker_cores,
            memory=worker_memory,
            workers=workers,
            worker_cores=worker_cores,
            worker_memory=worker_memory,
        )

    async def watch(self, task):
        logs = self.cluster.logs(task)
        got_token = False
        for log in logs:
            if not got_token and TOKEN_STR in log:
                pos = log.find(TOKEN_STR) + len(TOKEN_STR)
                token = log[pos:pos+TOKEN_LEN]
                got_token = True
                self.display_url(task, token)

    def display_url(self, task, token):
        print('notebook ready. available at:')

        url = task.routes['/']['url']
        print(f'{url}{TOKEN_STR}{token}')
