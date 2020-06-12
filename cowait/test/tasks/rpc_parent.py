from cowait.tasks import Task, rpc
from .rpc_child import RpcChild


class RpcParent(Task):
    def init(self):
        self.called = False

    async def run(self):
        child = RpcChild()
        print('waiting for child init...')
        await child.wait_for_init()

        print('calling child rpc')
        rpc_result = await child.echo(value=1)
        assert rpc_result['value'] == 1

        print('all done')
        task_result = await child
        assert task_result['called']

        # expect to receive rpc call from child
        assert self.called

    @rpc
    async def set_called(self) -> int:
        self.called = True
        return 1337
