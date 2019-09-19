import os
import json
import docker
import socket
from pipeline.tasks import Task, TaskContext, TaskDefinition
from .cluster import ClusterProvider


class DockerTask(Task):
    def __init__(self, cluster: ClusterProvider, taskdef: TaskDefinition, container):
        super().__init__(TaskContext(
            cluster=cluster,
            taskdef=taskdef,
            upstream=None,
        ))
        self.container = container



class DockerProvider(ClusterProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.docker = docker.from_env()
        self.tasks = { }


    def spawn(self, taskdef: TaskDefinition):
        container = self.docker.containers.run(
            image = taskdef.image,
            detach = True,
            name = taskdef.id,
            hostname = taskdef.id,
            network = 'tasks',
            environment = {
                **taskdef.env,
                'TASK_CLUSTER_PROVIDER': 'docker',
                'TASK_CLUSTER_ARGUMENTS': '{}',
                'TASK_DEFINITION': json.dumps(taskdef.serialize()),
            },
            volumes={
                '/var/run/docker.sock': {
                    'bind': '/var/run/docker.sock', 
                    'mode': 'ro',
                },
            },
        )
        task = DockerTask(self, taskdef, container)
        self.tasks[taskdef.id] = task
        return task


    def destroy(self, task_id):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            print('destroy', task_id)
            task.container.stop()
            task.container.remove()


    def logs(self, task: DockerTask):
        for log in task.container.logs(stream=True):
            if log[-1] == 10: # newline
                log = log[:-1]
            yield str(log, encoding='utf-8')


    def wait(self, task: DockerTask):
        pass