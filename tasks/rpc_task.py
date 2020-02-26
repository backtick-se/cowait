from pipeline.tasks import Task, sleep, rpc
from pipeline.tasks.components import HttpComponent


class RpcTask(Task):
    async def before(self, inputs: dict) -> None:
        inputs = await super().before(inputs)

        # create web server
        self.http = HttpComponent(self)
        self.http.start()

        return inputs

    async def run(self, **inputs):
        while True:
            await sleep(1)

    @rpc
    async def rpc_test(self, param):
        print('rpc!', param)
        return param
