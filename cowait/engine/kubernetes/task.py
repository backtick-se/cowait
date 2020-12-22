from cowait.tasks import TaskDefinition, RemoteTask
from cowait.engine.cluster import ClusterProvider


class KubernetesTask(RemoteTask):
    def __init__(
        self,
        cluster: ClusterProvider,
        taskdef: TaskDefinition,
        pod,
    ):
        super().__init__(
            cluster=cluster,
            taskdef=taskdef,
        )
        self.pod = pod
        self.ip = self.pod.status.pod_ip

    def __str__(self):
        return f'KubernetesTask({self.id}, {self.status}, {self.inputs})'
