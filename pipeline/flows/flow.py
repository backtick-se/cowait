import socket
from typing import Any
from abc import abstractmethod
from pipeline.network import PullSocket
from pipeline.tasks import Task, TaskContext, TaskDefinition, ReturnException, TaskError


PORT = 1337


def get_local_connstr():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return f'tcp://{local_ip}:{PORT}'


class Flow(Task):
    """ Serves as the base class for all tasks with children """


    def __init__(self, context: TaskContext):
        super().__init__(context)
        self.tasks = { }


    def run(self, **inputs) -> Any:
        # server socket
        daemon = PullSocket(f'tcp://*:{PORT}')

        # create tasks
        self.plan(**inputs)

        # initialize
        self.init()

        # run scheduler
        try:
            while True:
                msg = daemon.recv()
                if self.handle(**msg):
                    self.upstream.msg(**msg)

        except ReturnException:
            # ensure triggering message is passed up:
            self.upstream.msg(**msg)

            # assemble & return result
            return self.result()


    def spawn(self, name: str, image: str = None, **inputs) -> Task:
        """
        Spawn a child task.

        Arguments:
            name (str): Task name
            image (str): Task image. Defaults to parent image.
            kwargs (dict): Input arguments
        """
        taskdef = TaskDefinition(
            name = name,
            inputs = inputs,
            image = image if image else self.image,
            parent = get_local_connstr(),
        )

        # notify parents of task creation
        self.upstream.init(taskdef=taskdef)

        task = self.cluster.spawn(taskdef)
        self.tasks[task.id] = task
        return task


    def handle(self, id: str, type: str, **msg) -> bool:
        if type == 'return':
            self.on_return(id, msg['result'])
        elif type == 'fail':
            self.on_fail(id, msg['error'])
        return True


    def init(self) -> None:
        """ Virtual initialization method. Called after plan() """
        pass


    def result(self) -> Any:
        """ Virtual method for creating a return value """
        return None

        
    @abstractmethod
    def plan(self, **inputs) -> None:
        """ Virtual method for scheduling subtasks """
        pass


    def on_return(self, id: str, result: Any) -> None:
        """ Return message handler """
        pass


    def on_fail(self, id: str, error: str) -> None:
        """ Fail message handler """
        raise TaskError(error)
