from __future__ import annotations
import json
from abc import abstractmethod
from typing import Iterable
from marshmallow import Schema, fields
from pipeline.tasks import TaskDefinition, RemoteTask
from pipeline.utils import EventEmitter
from .const import ENV_TASK_CLUSTER, ENV_TASK_DEFINITION


class ClusterProvider(EventEmitter):
    def __init__(self, type, args={}):
        super().__init__()
        self.type = type
        self.args = args

    @abstractmethod
    def spawn(self, taskdef: TaskDefinition) -> RemoteTask:
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
    def wait(self, task: RemoteTask) -> None:
        """ Wait for task to exit """
        pass

    @abstractmethod
    def logs(self, task: RemoteTask) -> Iterable[str]:
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
