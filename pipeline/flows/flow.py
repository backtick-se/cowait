import socket
from typing import Any
from abc import abstractmethod
from pipeline.network import PullSocket
from pipeline.tasks import *
from .ops import Await, Join


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
        self.daemon = PullSocket(f'tcp://*:{PORT}')

        # create tasks
        return self.plan(**inputs)


    def op(self, op):
        try:
            while True:
                msg = self.daemon.recv()
                if op.handle(**msg) and self.handle(**msg):
                    self.upstream.msg(**msg)

        except ReturnException:
            # ensure triggering message is passed up:
            self.upstream.msg(**msg)

            # assemble & return result
            return op.result()


    def task(self, name: str, image: str = None, **inputs) -> Task:
        """
        Spawn a child task.

        Arguments:
            name (str): Task name
            image (str): Task image. Defaults to parent image.
            kwargs (dict): Input arguments
        """

        # await any inputs
        arguments = { }
        for key, value in inputs.items():
            if isinstance(value, TaskFuture):
                value = Await(value)
            arguments[key] = value

        taskdef = TaskDefinition(
            name = name,
            inputs = arguments,
            image = image if image else self.image,
            parent = get_local_connstr(),
        )

        # notify parents of task creation
        self.upstream.init(taskdef=taskdef)

        task = self.cluster.spawn(taskdef)
        future = TaskFuture(self, task)
        self.tasks[task.id] = future
        return future


    def define(self, name: str, image: str = None, **inputs):
        base_inputs = inputs
        def task(**inputs):
            return self.task(
                name=name,
                image=image,
                **{
                    **base_inputs,
                    **inputs,
                },
            )
        return task


    @abstractmethod
    def plan(self, **inputs):
        """ Virtual method for scheduling subtasks """
        return None


    def handle(self, id: str, type: str, **msg) -> bool:
        if not id in self.tasks:
            return True

        if type == 'return':
            result = msg['result']
            self.tasks[id].done(result)

        elif type == 'fail':
            error = msg['error']
            self.tasks[id].fail(error)

        return True


    def join(self):
        self.op(Join(self.tasks.values()))