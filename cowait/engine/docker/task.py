from cowait.tasks import TaskDefinition, RemoteTask
from cowait.engine.cluster import ClusterProvider


class DockerTask(RemoteTask):
    def __init__(
        self,
        cluster: ClusterProvider,
        taskdef: TaskDefinition,
        container
    ):
        super().__init__(
            cluster=cluster,
            taskdef=taskdef,
        )
        self.container = container
        self.ip = taskdef.id  # id should be routable within docker

    def __str__(self):
        return f'DockerTask({self.id}, {self.status}, {self.inputs}, {self.container.id[:10]})'
