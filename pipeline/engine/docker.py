import docker
from pipeline.tasks import TaskDefinition, RemoteTask
from .cluster import ClusterProvider
from .const import LABEL_TASK_ID, LABEL_PARENT_ID
from .routers import LocalPortRouter

DEFAULT_NETWORK = 'tasks'


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


class DockerProvider(ClusterProvider):
    def __init__(self, args={}):
        super().__init__('docker', args)
        self.docker = docker.from_env()
        self.router = LocalPortRouter(self)

    @property
    def network(self):
        return self.args.get('network', DEFAULT_NETWORK)

    def spawn(self, taskdef: TaskDefinition) -> DockerTask:
        self.ensure_network()

        self.emit_sync('prepare', taskdef=taskdef)

        container = self.docker.containers.run(
            detach=True,
            image=taskdef.image,
            name=taskdef.id,
            hostname=taskdef.id,
            network=self.network,
            ports=self.create_ports(taskdef),
            environment=self.create_env(taskdef),
            volumes={
                # this is the secret sauce that allows us to create new
                # tasks as sibling containers
                '/var/run/docker.sock': {
                    'bind': '/var/run/docker.sock',
                    'mode': 'ro',
                },
            },
            labels={
                LABEL_TASK_ID: taskdef.id,
                LABEL_PARENT_ID: taskdef.parent,
            },
        )

        print('~~ created docker container with id',
              container.id[:12], 'for task', taskdef.id)

        task = DockerTask(self, taskdef, container)
        self.emit_sync('spawn', task=task)
        return task

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
            container_id = container.id[:12]
            print(f'~~ kill {container_task_id} ({container_id})')

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

    def ensure_network(self):
        try:
            self.docker.networks.get(self.network)
        except docker.errors.NotFound:
            print('~~ creating docker network', self.network)
            self.docker.networks.create(
                name=self.network,
                check_duplicate=False,
                driver='bridge',
                labels={
                    'pipeline': 1,
                })

    def create_ports(self, taskdef):
        return taskdef.ports

    def find_agent(self):
        try:
            self.docker.containers.get('agent')
            return 'ws://agent/ws'
        except docker.errors.NotFound:
            return None
