import asyncio
from cowait.tasks import TaskDefinition, RemoteTask
from cowait.engine.cluster import ClusterProvider
from cowait.engine.errors import TaskCreationError
from .pod import pod_is_running, pod_is_terminated, pod_is_creating, \
    pod_is_unschedulable, pod_image_pull_failed


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

    async def wait_for_scheduling(self):
        poll_interval = 0
        while True:
            await asyncio.sleep(poll_interval)
            pod = self.cluster.get_task_pod(self.id)

            if pod_is_running(pod):
                break

            if pod_is_creating(pod):
                poll_interval = 1
                continue
            
            if pod_is_terminated(pod):
                raise TaskCreationError('Task terminated')
            
            if pod_image_pull_failed(pod):
                self.cluster.kill(self.id)
                raise TaskCreationError('Image pull failed')

            if pod_is_unschedulable(pod):
                poll_interval = 10
                print('warning: task', self.id, 'is unschedulable')
                continue

