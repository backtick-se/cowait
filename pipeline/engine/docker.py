import os
import json
import docker
import socket
from .task import TaskDefinition, Task
from .cluster import ClusterProvider


class DockerTask(Task):
    def __init__(self, cluster, taskdef, container):
        super().__init__(cluster, taskdef)
        self.container = container



class DockerProvider(ClusterProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.docker = docker.from_env()
        self.hostname = os.environ.get('HOSTNAME', 'ROOT')


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
                'TASK_DEFINITION': json.dumps(taskdef.serialize()),
                'TASK_PARENT_HOST': self.hostname,
            },
            volumes={
                '/var/run/docker.sock': {
                    'bind': '/var/run/docker.sock', 
                    'mode': 'ro',
                },
            },
        )
        print('spawned docker container with id', container.id)
        return DockerTask(self, taskdef, container)


    def logs(self, task: DockerTask):
        for log in task.container.logs(stream=True):
            if log[-1] == 10: # newline
                log = log[:-1]
            yield str(log, encoding='utf-8')


    def wait(self, task: DockerTask):
        pass