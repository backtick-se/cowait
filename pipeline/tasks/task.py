import os
from typing import Any
from .definition import TaskDefinition


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
        self.cluster = cluster
        self.node = node

    async def before(self, inputs: dict) -> dict:
        return inputs

    async def run(self, **inputs: dict) -> Any:
        pass

    async def after(self, inputs: dict) -> Any:
        pass

    async def stop(self) -> None:
        """
        Abort task execution.

        Raises:
            StopException: Used to stop execution.
        """
        await self.node.api.stop()
        os._exit(1)

    def __str__(self) -> str:
        return f'Task({self.id}, {self.name})'
