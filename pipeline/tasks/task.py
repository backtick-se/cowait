from typing import Any
from .errors import StopException
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

    def run(self, **inputs: dict) -> Any:
        pass

    def stop(self) -> None:
        """
        Abort task execution.

        Raises:
            StopException: Used to stop execution.
        """
        raise StopException()

    def __str__(self) -> str:
        return f'Task({self.id}, {self.name})'
