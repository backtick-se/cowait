import asyncio
from cowait.tasks import TaskDefinition, RemoteTask
from cowait.engine.cluster import ClusterProvider
from cowait.engine.errors import TaskCreationError
from .pod import pod_is_ready
from .errors import PodUnschedulableError, PodTerminatedError, ImagePullError


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

            try:
                if pod_is_ready(pod):
                    break
                else:
                    poll_interval = 1

            except PodUnschedulableError as e:
                poll_interval = 10
                print('warning: task', self.id, 'is unschedulable:', str(e))

            except PodTerminatedError:
                raise TaskCreationError('Task terminated') from None
            
            except ImagePullError:
                self.cluster.kill(self.id)
                raise TaskCreationError('Image pull failed')

