import asyncio
from typing import Any
from abc import abstractmethod
from pipeline.tasks import Task, TaskContext, TaskDefinition
from pipeline.network import get_local_connstr
from pipeline.network.service import TaskList


class Flow(Task):
    """ Serves as the base class for all tasks with children """

    def __init__(self, context: TaskContext):
        super().__init__(context)
        self.tasks = { }
        self.tasklist = TaskList()


    def handle(self, id: str, type: str, **msg):
        if type == 'return' and id in self.tasks: 
            future = self.tasks[id]
            future.set_result(future.task)
        if type == 'fail' and id in self.tasks:
            future = self.tasks[id]
            future.set_exception(msg['error'])


    async def run(self, **inputs) -> Any:
        self.node.bind('tcp://*:1337')
        self.node.attach(self)

        asyncio.create_task(self.node.serve())

        try:
            await self.plan(**inputs)

            # check return value for futures and await them? 🤔

        except Exception as e:
            print('destroyig children due to error...')

            # ask the cluster to destroy any children
            children = self.cluster.destroy_children(self.id)

            # send a stop message upstream for each killed task
            for child_id in children:
                self.node.send_stop(id=child_id)

            # pass on to task level error handling
            raise e


    async def task(self, name: str, image: str = None, **inputs) -> asyncio.Future:
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
            if isinstance(value, asyncio.Future):
                value = await value
            arguments[key] = value

        taskdef = TaskDefinition(
            name = name,
            inputs = arguments,
            parent = self.id,
            image = image if image else self.image,
            upstream = get_local_connstr(),
        )

        task = self.cluster.spawn(taskdef)


        # return a future
        future = asyncio.Future()
        future.task = task
        self.tasks[task.id] = future
        return await future


    def define(self, name: str, image: str = None, **inputs):
        base_inputs = inputs
        async def task(**inputs):
            return await self.task(
                name=name,
                image=image,
                **{
                    **base_inputs,
                    **inputs,
                },
            )
        return task


    @abstractmethod
    async def plan(self, **inputs):
        """ Virtual method for scheduling subtasks """
        return None
