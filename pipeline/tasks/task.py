import os
from typing import Any
from datetime import datetime
from pipeline.network import get_local_connstr
from .definition import TaskDefinition
from .components import TaskManager, RpcComponent, rpc


class Task(TaskDefinition):
    """
    Task base class.
    """

    def __init__(
        self,
        taskdef,
        cluster,
        node,
    ):
        kwargs = taskdef.serialize()
        super().__init__(**kwargs)
        self.node = node
        self.cluster = cluster
        self.subtasks = TaskManager(self)
        self.rpc = RpcComponent(self)

    def __str__(self) -> str:
        return f'Task({self.id}, {self.name})'

    async def before(self, inputs: dict) -> dict:
        return inputs

    async def run(self, **inputs: dict) -> Any:
        pass

    async def after(self, inputs: dict) -> Any:
        pass

    @rpc
    async def stop(self) -> None:
        """
        Abort task execution.

        Raises:
            StopException: Used to stop execution.
        """
        print('\n~~ STOPPED ~~')

        await self.node.api.stop()
        for task in self.subtasks.values():
            await task.stop()

        os._exit(1)

    def spawn(
        self,
        name: str,
        id: str = None,
        image: str = None,
        ports: dict = {},
        routes: dict = {},
        inputs: dict = {},
        meta: dict = {},
        env: dict = {},
        cpu: str = '0',
        memory: str = '0',
        owner: str = '',
        **kwargs: dict,
    ) -> 'Task':
        """
        Spawn a subtask.

        Arguments:
            name (str): Task name
            image (str): Task image. Defaults to the current task image.
            kwargs (dict): Input arguments
        """

        if not isinstance(name, str) and issubclass(name, Task):
            name = name.__module__

        # todo: throw error if any input is a coroutine

        task = self.cluster.spawn(TaskDefinition(
            name=name,
            parent=self.id,
            image=image if image else self.image,
            upstream=get_local_connstr(),
            meta=meta,
            ports=ports,
            routes=routes,
            inputs={
                **inputs,
                **kwargs,
            },
            env={
                **self.env,
                **env,
            },
        ))

        # register with subtask manager
        self.subtasks.watch(task)

        return task
