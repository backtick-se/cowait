import socket
from typing import Any
from abc import abstractmethod
from pipeline.tasks import *
from pipeline.network import get_local_connstr
from .ops import Await, Join
from .server import FlowServer
from .tasklist import TaskList
from pipeline.protocol import StopMsg


class Flow(Task):
    """ Serves as the base class for all tasks with children """

    def __init__(self, context: TaskContext):
        super().__init__(context)
        self.tasks = { }
        self.tasklist = TaskList()


    def run(self, **inputs) -> Any:
        print('setting up flow daemon')
        self.node.bind('tcp://*:1337')
        self.node.attach(self)
        self.node.attach(self.tasklist)

        try:
            return self.plan(**inputs)

        except Exception as e:
            print('destroyig children due to error...')

            # ask the cluster to destroy any children
            children = self.cluster.destroy_children(self.id)

            # send a stop message upstream for each killed task
            for child_id in children:
                self.node.send_stop(id=child_id)

            # pass on to task level error handling
            raise e


    def op(self, op):
        print('serving operation', op)
        try:
            self.node.attach(op)
            self.node.serve()
        except ReturnException:
            self.node.detach(op)
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
            parent_id = self.id,
            image = image if image else self.image,
            upstream = get_local_connstr(),
        )

        task = self.cluster.spawn(taskdef)


        # return a future
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
            print('flow child', id, 'completed')
            self.tasks[id].done(result)

        elif type == 'fail':
            error = msg['error']
            print('flow child', id, 'failed')
            self.tasks[id].fail(error)

        return True


    def join(self):
        self.op(Join(self.tasks.values()))