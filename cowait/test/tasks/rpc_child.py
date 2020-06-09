from cowait.tasks import Task, rpc, sleep


class RpcChild(Task):
    def init(self):
        self.called = False

    async def run(self) -> dict:
        print('waiting for call from parent...')
        for i in range(0, 5):
            if self.called:
                break
            await sleep(1)

        return {
            'called': self.called
        }

    @rpc
    async def echo(self, **params) -> dict:
        print('echo', params)
        self.called = True
        return params
