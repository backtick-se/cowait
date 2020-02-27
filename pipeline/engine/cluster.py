from __future__ import annotations
import json
import asyncio
from abc import abstractmethod
from typing import Iterable
from marshmallow import Schema, fields
from concurrent.futures import Future
from websockets.exceptions import ConnectionClosed
from pipeline.tasks import TaskDefinition
from pipeline.utils import EventEmitter
from .const import ENV_TASK_CLUSTER, ENV_TASK_DEFINITION


class ClusterTask(TaskDefinition):
    def __init__(self, taskdef: TaskDefinition, cluster: ClusterProvider):
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
        try:
            await self.call('stop')
        except ConnectionClosed:
            pass

    def __getattr__(self, method):
        async def magic_rpc(**kwargs):
            return await self.call(method, kwargs)
        return magic_rpc


class ClusterProvider(EventEmitter):
    def __init__(self, type, args={}):
        super().__init__()
        self.type = type
        self.args = args

    @abstractmethod
    def spawn(self, taskdef: TaskDefinition) -> ClusterTask:
        """ Spawn a task in the cluster """
        pass

    @abstractmethod
    def destroy(self, task_id: str) -> None:
        """ Destroy a task """
        pass

    @abstractmethod
    def destroy_all(self) -> None:
        pass

    @abstractmethod
    def destroy_children(self, parent_id: str) -> None:
        pass

    @abstractmethod
    def wait(self, task: ClusterTask) -> None:
        """ Wait for task to exit """
        pass

    @abstractmethod
    def logs(self, task: ClusterTask) -> Iterable[str]:
        """ Stream logs from task """
        pass

    def serialize(self) -> dict:
        """ Serialize ClusterProvider into a dict """
        return ClusterProviderSchema().dump(self)

    @staticmethod
    def deserialize(provider: dict) -> ClusterProvider:
        """ Deserialize ClusterProvider from a dict """
        return ClusterProviderSchema().load(provider)

    def create_env(self, taskdef: TaskDefinition) -> dict:
        """
        Create a container environment dict from a task definition.

        Arguments:
            taskdef (TaskDefinition): Task definition

        Returns:
            env (dict): Environment variable dict
        """
        return {
            **taskdef.env,
            ENV_TASK_CLUSTER:    json.dumps(self.serialize()),
            ENV_TASK_DEFINITION: json.dumps(taskdef.serialize()),
        }

    def find_agent(self):
        return None


class ClusterProviderSchema(Schema):
    type = fields.Str(required=True)
    args = fields.Dict(missing={})
