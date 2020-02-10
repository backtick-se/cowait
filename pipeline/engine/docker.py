import docker
from pipeline.tasks import TaskDefinition
from .cluster import ClusterProvider, ClusterTask

DEFAULT_NETWORK = 'tasks'
LABEL_TASK_ID = 'pipeline/task'
LABEL_PARENT_ID = 'pipeline/parent'


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

    @property
    def network(self):
        return self.args.get('network', DEFAULT_NETWORK)

    def spawn(self, taskdef: TaskDefinition) -> DockerTask:
        container = self.docker.containers.run(
            detach=True,
            image=taskdef.image,
            name=taskdef.id,
            hostname=taskdef.id,
            network=self.network,
            environment=self.create_env(taskdef),
            volumes={
                '/var/run/docker.sock': {
                    'bind': '/var/run/docker.sock',
                    'mode': 'ro',
                },
            },
            labels={
                LABEL_TASK_ID: taskdef.id,
                LABEL_PARENT_ID: taskdef.parent,
            },
            ports=taskdef.ports,
        )

        print('~~ created docker container with id',
              container.id[:12], 'for task', taskdef.id)

        return DockerTask(self, taskdef, container)

    def list_all(self) -> list:
        """ Returns a list of all running tasks """
        containers = self.docker.containers.list(
            filters={
                'label': LABEL_TASK_ID,
            },
        )
        return list(map(lambda c: c.labels[LABEL_TASK_ID], containers))

    def destroy_all(self) -> None:
        """ Destroys all running tasks """
        containers = self.docker.containers.list(
            filters={
                'label': LABEL_TASK_ID,
            },
        )

        for container in containers:
            container.remove(force=True)

    def find_child_containers(self, parent_id: str) -> list:
        """ Finds all child containers of a given task id """
        return self.docker.containers.list(
            filters={
                'label': f'{LABEL_PARENT_ID}={parent_id}',
            },
        )

    def destroy_children(self, parent_id: str) -> list:
        """ Destroy all child tasks of a given task id """
        children = self.find_child_containers(parent_id)

        tasks = []
        for child in children:
            tasks += self.destroy(child.labels[LABEL_TASK_ID])

        return tasks

    def destroy(self, task_id):
        """ Destroy a specific task id and all its descendants """

        # optimization: grab a list of all tasks at once, instead of querying
        # for every child.

        def kill_family(container):
            container_task_id = container.labels[LABEL_TASK_ID]
            print('~~ docker kill', container.id[:12],
                  '->', container_task_id)

            children = self.find_child_containers(container_task_id)
            kills = []
            for child in children:
                kills += kill_family(child)

            try:
                container.remove(force=True)
            except docker.errors.NotFound:
                pass

            kills.append(task_id)
            return kills

        try:
            container = self.docker.containers.get(task_id)
            return kill_family(container)
        except docker.errors.NotFound:
            return [task_id]

    def logs(self, task: DockerTask):
        """ Stream task logs """
        for log in task.container.logs(stream=True):
            if log[-1] == 10:  # newline
                log = log[:-1]
            yield str(log, encoding='utf-8')

    def wait(self, task: DockerTask):
        """ Wait for a task to finish """
        raise NotImplementedError()
