from pipeline.tasks import Task, sleep, rpc


class RpcTask(Task):
    async def run(self, **inputs):
        while True:
            await sleep(1)

    @rpc
    async def rpc_test(self, param):
        print('rpc!', param)
        return param
