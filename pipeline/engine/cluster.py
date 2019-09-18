from abc import ABC, abstractmethod
from .task import Task, TaskDefinition


class ClusterProvider(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()


    @abstractmethod
    def spawn(self, taskdef: TaskDefinition) -> Task:
        pass

    
    @abstractmethod
    def wait(self, task: Task):
        pass


    @abstractmethod
    def logs(self, task: Task):
        pass