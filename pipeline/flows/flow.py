import asyncio
from typing import Any
from abc import abstractmethod
from pipeline.tasks import Task, TaskDefinition, TaskError
from pipeline.network import get_local_connstr, PORT


class Flow(Task):
    """ Serves as the base class for all tasks with children """

    def handle(self, id: str, type: str, **msg):
        # complete future when we get a return message from a subtask
        if type == 'return' and id in self.tasks:
            future = self.tasks[id]
            if not future.done():
                future.set_result(msg['result'])

        # fail future when we get an error message from a subtask
        if type == 'fail' and id in self.tasks:
            future = self.tasks[id]
            if not future.done():
                future.set_exception(TaskError(msg['error']))

    async def run(self, **inputs) -> Any:
        self.tasks = {}
        self.node.bind(PORT)
        self.node.attach(self)

        # run task daemon in the background
        asyncio.create_task(self.node.serve())

        try:
            return await self.plan(**inputs)
        except Exception as e:
            self.stop()
            raise e

    def stop(self):
        # ask the cluster to destroy any children
        # children = self.cluster.destroy_children(self.id)

        # send a stop message upstream for each killed task
        # for child_id in children:
        #    self.node.send_stop(id=child_id)
        pass

    async def task(
        self,
        name: str,
        image: str = None,
        env: dict = {},
        **inputs,
    ) -> asyncio.Future:
        """
        Spawn a child task.

        Arguments:
            name (str): Task name
            image (str): Task image. Defaults to parent image.
            kwargs (dict): Input arguments
        """

        # await any inputs
        for key, value in inputs.items():
            if isinstance(value, asyncio.Future):
                inputs[key] = await value

        taskdef = TaskDefinition(
            name=name,
            inputs=inputs,
            parent=self.id,
            image=image if image else self.image,
            upstream=get_local_connstr(),
            config=self.config,
            env={
                **self.env,
                **env,
            },
        )

        task = self.cluster.spawn(taskdef)

        # return a future
        future = asyncio.Future()
        self.tasks[task.id] = future
        return await future

    def define(
        self,
        name: str,
        image: str = None,
        env: dict = {},
        **inputs,
    ) -> callable:
        base_inputs = inputs

        async def task(**inputs):
            return await self.task(
                name=name,
                image=image,
                env=env,
                **base_inputs,
                **inputs,
            )
        return task

    @abstractmethod
    async def plan(self, **inputs):
        """ Virtual method for scheduling subtasks """
        return None
