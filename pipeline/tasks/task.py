from abc import ABC
from typing import Any, Iterable
from .errors import StopException
from .task_context import TaskContext


class Task(ABC):
    """
    Task base class.

    Attributes:
        id (str): Task id
        name (str): Task import name
        image (str): Task image
        inputs (dict): Input arguments
        parent (str): Parent task id
        cluster (ClusterProvider): Cluster provider
        upstream (UpstreamConnector): Upstream connection
    """

    def __init__(self, context: TaskContext):
        """
        Arguments:
            context (TaskContext): Task execution context
        """
        self.id       = context.id
        self.name     = context.name
        self.image    = context.image
        self.inputs   = context.inputs
        self.parent   = context.parent
        self.cluster  = context.cluster
        self.upstream = context.upstream


    def run(self, **inputs: dict) -> Any:
        pass


    def stop(self) -> None:
        """ 
        Abort task execution.

        Raises:
            StopException: Used to stop execution.
        """
        raise StopException()
