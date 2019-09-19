from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Iterable
from marshmallow import Schema, fields
from pipeline.tasks import Task, TaskContext, TaskDefinition
from .const import ENV_TASK_CLUSTER, ENV_TASK_DEFINITION


class ClusterProvider(ABC):
    def __init__(self, type, args = { }):
        """
        """
        self.type = type
        self.args = args


    @abstractmethod
    def spawn(self, taskdef: TaskDefinition) -> Task:
        """ Spawn a task in the cluster """
        pass


    @abstractmethod
    def destroy(self, task_id: str) -> None:
        """ Destroy a task """
        pass

    
    @abstractmethod
    def wait(self, task: Task) -> None:
        """ Wait for task to exit """
        pass


    @abstractmethod
    def logs(self, task: Task) -> Iterable[str]:
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



class ClusterProviderSchema(Schema):
    type = fields.Str(required=True)
    args = fields.Dict(missing={})
