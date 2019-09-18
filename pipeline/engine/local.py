from .cluster import ClusterProvider
from .task import Task, TaskDefinition

class LocalCluster(ClusterProvider):
    def spawn(self, taskdef: TaskDefinition) -> Task:
        # just instantiate the class directly!! lol
        pass