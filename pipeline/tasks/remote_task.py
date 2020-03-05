from __future__ import annotations
import asyncio
from concurrent.futures import Future
from .definition import TaskDefinition


class RemoteTask(TaskDefinition):
    def __init__(self, taskdef: TaskDefinition, cluster):
        kwargs = taskdef.serialize()
        super().__init__(**kwargs)
        self.conn = None
        self.nonce = 0
        self.cluster = cluster
        self.future = Future()
        self.awaitable = asyncio.wrap_future(self.future)

    def __await__(self):
        return self.awaitable.__await__()

    def destroy(self):
        self.cluster.destroy(self.id)

    async def wait_for_init(self, timeout=30):
        slept = 0
        interval = 0.2
        while self.conn is None and slept < timeout:
            await asyncio.sleep(interval)
            slept += interval

    async def call(self, method, args={}):
        if self.conn is None:
            raise RuntimeError('Task connection not yet available')
        return await self.conn.rpc.call(method, args)

    async def stop(self):
        # special case RPC - it always causes a send exception
        await self.call('stop')

    def __getattr__(self, method):
        async def magic_rpc(**kwargs):
            return await self.call(method, kwargs)
        return magic_rpc
