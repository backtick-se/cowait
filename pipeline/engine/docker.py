import docker
from pipeline.tasks import TaskDefinition
from .cluster import ClusterProvider, ClusterTask

NETWORK = 'tasks'


class DockerTask(ClusterTask):
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


class DockerProvider(ClusterProvider):
    def __init__(self, args={}):
        super().__init__('docker', args)
        self.docker = docker.from_env()

    def spawn(self, taskdef: TaskDefinition) -> DockerTask:
        ports = taskdef.inputs.get('ports', None)
        container = self.docker.containers.run(
            detach=True,
            image=taskdef.image,
            name=taskdef.id,
            hostname=taskdef.id,
            network=NETWORK,
            environment=self.create_env(taskdef),
            volumes={
                '/var/run/docker.sock': {
                    'bind': '/var/run/docker.sock',
                    'mode': 'ro',
                },
            },
            labels={
                'task': taskdef.id,
                'task_parent': taskdef.parent,
            },
            ports=ports,
        )

        print('~~ created docker container with id',
              container.id[:12], 'for task', taskdef.id)

        return DockerTask(self, taskdef, container)

    def list_all(self) -> list:
        """ Returns a list of all running tasks """
        containers = self.docker.containers.list(
            filters={
                'label': 'task',
            },
        )
        return map(lambda c: c.labels['task'], containers)

    def destroy_all(self) -> None:
        """ Destroys all running tasks """
        containers = self.docker.containers.list(
            filters={
                'label': 'task',
            },
        )

        for container in containers:
            container.remove(force=True)

    def find_child_containers(self, parent_id: str) -> list:
        """ Finds all child containers of a given task id """
        return self.docker.containers.list(
            filters={
                'label': f'task_parent={parent_id}',
            },
        )

    def destroy_children(self, parent_id: str) -> list:
        """ Destroy all child tasks of a given task id """
        children = self.find_child_containers(parent_id)

        tasks = []
        for child in children:
            tasks += self.destroy(child.labels['task'])

        return tasks

    def destroy(self, task_id):
        """ Destroy a specific task id and all its descendants """
        def kill_family(container):
            container_task_id = container.labels['task']
            print('~~ docker kill', container.id[:12],
                  '->', container_task_id)

            children = self.find_child_containers(container_task_id)
            kills = []
            for child in children:
                kills += kill_family(child)

            try:
                container.remove(force=True)
            except docker.errors.NotFound:
                print('~~ docker: kill: task', task_id,
                      'container not found:', container.id[:12])

            kills.append(task_id)
            return kills

        container = self.docker.containers.get(task_id)
        return kill_family(container)

    def logs(self, task: DockerTask):
        """ Stream task logs """
        for log in task.container.logs(stream=True):
            if log[-1] == 10:  # newline
                log = log[:-1]
            yield str(log, encoding='utf-8')

    def wait(self, task: DockerTask):
        """ Wait for a task to finish """
        raise NotImplementedError()
