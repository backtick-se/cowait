from abc import ABC, abstractmethod
from pipeline.tasks import Task, TaskContext, TaskDefinition


class ClusterProvider(ABC):
    def __init__(self, *args, **kwargs):
        pass


    @abstractmethod
    def spawn(self, taskdef: TaskDefinition) -> Task:
        pass

    
    @abstractmethod
    def wait(self, task: Task):
        pass


    @abstractmethod
    def logs(self, task: Task):
        pass