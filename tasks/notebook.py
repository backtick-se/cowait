from pipeline.tasks.container import ContainerTask

TOKEN_STR = '?token='
TOKEN_LEN = 48


class JupyterTask(ContainerTask):
    async def run(self):
        print('creating jupyter notebook...')
        await super().run(
            name='jupyter',
            image='jupyter/base-notebook:latest',
            routes={
                '/': 8888,
            },
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
