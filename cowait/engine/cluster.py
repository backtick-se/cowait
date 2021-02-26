from __future__ import annotations
from abc import abstractmethod
from typing import Iterable
from cowait.tasks import TaskDefinition, RemoteTask
from cowait.utils import EventEmitter
from .const import ENV_TASK_CLUSTER, ENV_TASK_DEFINITION, ENV_GZIP_ENABLED, MAX_ENV_LENGTH
from .errors import ProviderError
from .utils import env_pack


class ClusterProvider(EventEmitter):
    def __init__(self, type, args={}):
        super().__init__()
        self.type = type
        self.args = args

    @abstractmethod
    def spawn(self, taskdef: TaskDefinition) -> RemoteTask:
        """ Spawn a task in the cluster """
        raise NotImplementedError()

    @abstractmethod
    def destroy(self, task_id: str) -> None:
        """ Destroy a task """
        raise NotImplementedError()

    @abstractmethod
    def destroy_all(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def destroy_children(self, parent_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def wait(self, task: RemoteTask) -> bool:
        """ Wait for task to exit. Returns True on clean exit. """
        raise NotImplementedError()

    @abstractmethod
    def logs(self, task_id: str) -> Iterable[str]:
        """ Stream logs from task """
        raise NotImplementedError()

    @abstractmethod
    def list_all(self) -> list:
        raise NotImplementedError()

    def serialize(self) -> dict:
        """ Serialize ClusterProvider into a dict """
        return {
            'type': self.type,
            **self.args,
        }

    def find_agent(self):
        return None

