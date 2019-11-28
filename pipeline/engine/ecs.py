import os
import time
import kubernetes
from typing import Dict
from kubernetes import client, config, watch
from pipeline.tasks import Task, TaskContext, TaskDefinition
from .const import ENV_TASK_CLUSTER
from .cluster import ClusterProvider


class ECSTask(Task):
    def __init__(self, cluster: ClusterProvider, taskdef: TaskDefinition, job, pod):
        super().__init__(TaskContext(
            cluster=cluster,
            taskdef=taskdef,
            node=None,
        ))
        self.job = job
        self.pod = pod


class ECSProvider(ClusterProvider):
    def __init__(self, args = { }):
        super().__init__('ecs', args)
        self.cluster = args.get('cluster')
        self.role = args.get('role')

    def spawn(self, taskdef: TaskDefinition, timeout=30) -> ECSTask:
        # create task definition
        # create task
        pass

    def destroy(self, task_id):
        raise NotImplementedError()

    def wait(self, task: ECSTask) -> None:
        while True:
            time.sleep(0.5)

    def logs(self, task: ECSTask):
        pass

    def destroy_all(self) -> None:
        raise NotImplementedError()

    def destroy_children(self, parent_id: str) -> list:
        raise NotImplementedError()
