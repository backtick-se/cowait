import docker
from pipeline.tasks import Task, TaskContext, TaskDefinition
from .cluster import ClusterProvider


class DockerTask(Task):
    def __init__(
        self,
        cluster: ClusterProvider,
        taskdef: TaskDefinition,
        container
    ):
        super().__init__(TaskContext(
            cluster=cluster,
            taskdef=taskdef,
            node=None,
        ))
        self.container = container


class DockerProvider(ClusterProvider):
    def __init__(self, args={}):
        super().__init__('docker', args)
        self.docker = docker.from_env()
        self.tasks = {}

    def spawn(self, taskdef: TaskDefinition):
        container = self.docker.containers.run(
            detach=True,
            image=taskdef.image,
            name=taskdef.id,
            hostname=taskdef.id,
            network='tasks',
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
        )
        print('~~ created docker container with id',
              container.id[:12], 'for task', taskdef.id)
        return DockerTask(self, taskdef, container)

    def destroy_all(self) -> None:
        containers = self.docker.containers.list(
            filters={
                'label': 'task',
            },
        )
        for container in containers:
            container.remove(force=True)

    def find_child_containers(self, parent_id: str) -> list:
        return self.docker.containers.list(
            filters={
                'label': f'task_parent={parent_id}',
            },
        )

    def destroy_children(self, parent_id: str) -> list:
        tasks = []
        children = self.find_child_containers(parent_id)
        for child in children:
            child = self.destroy(child.labels['task'])
            tasks += child
        return tasks

    def destroy(self, task_id):
        def kill_family(container):
            kills = []
            container_task_id = container.labels['task']
            print('~~ docker: kill', container_task_id,
                  '->', container.id[:12])

            children = self.find_child_containers(container_task_id)
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
        for log in task.container.logs(stream=True):
            if log[-1] == 10:  # newline
                log = log[:-1]
            yield str(log, encoding='utf-8')

    def wait(self, task: DockerTask):
        raise NotImplementedError()
