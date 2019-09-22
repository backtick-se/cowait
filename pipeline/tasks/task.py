from abc import ABC
from typing import Any, Iterable
from datetime import datetime
from marshmallow import Schema, fields
from .errors import StopException
from .context import TaskContext


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
        self.upstream = context.upstream
        self.cluster  = context.cluster
        self.node     = context.node


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
