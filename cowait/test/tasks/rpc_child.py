from cowait.tasks import Task, rpc, sleep


class RpcChild(Task):
    def init(self):
        self.called = False

    async def run(self):
        await sleep(3)
        return {
            'called': self.called
        }

    @rpc
    async def echo(self, **params):
        self.called = True
        return params
