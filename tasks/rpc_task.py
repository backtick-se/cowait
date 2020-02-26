from pipeline.tasks import Flow, sleep
from pipeline.tasks.components import HttpComponent, RpcComponent, rpc


class RpcTask(Flow):
    async def before(self, inputs: dict) -> None:
        inputs = await super().before(inputs)

        # create web server
        self.http = HttpComponent(self)

        # create rpc handler
        self.rpc = RpcComponent(self)

        self.http.start()
        return inputs

    async def run(self, **inputs):
        while True:
            await sleep(1)

    @rpc
    async def rpc_test(self, param):
        print('rpc!', param)
        return param

    @rpc
    async def kill(self):
        print('aborted by rpc')
        await self.stop()
