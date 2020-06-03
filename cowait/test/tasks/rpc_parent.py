from cowait.tasks import Task
from .rpc_child import RpcChild


class RpcParent(Task):
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
