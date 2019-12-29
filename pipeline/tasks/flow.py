import asyncio
from typing import Any
from abc import abstractmethod
from pipeline.tasks import Task, TaskDefinition, TaskError
from pipeline.network import get_local_connstr, PORT


class Flow(Task):
    """ Serves as the base class for all tasks with children """

    def handle_downstream(self, **msg: dict) -> bool:
        pass

    def handle_upstream(self, id: str, type: str, **msg: dict) -> bool:
        # complete future when we get a return message from a subtask
        if type == 'return' and id in self.tasks:
            task = self.tasks[id]
            if not task.result.done():
                task.result.set_result(msg['result'])

        # fail future when we get an error message from a subtask
        if type == 'fail' and id in self.tasks:
            task = self.tasks[id]
            if not task.result.done():
                task.result.set_exception(TaskError(msg['error']))

        return True

    async def before(self, inputs):
        self.tasks = {}
        self.node.bind(PORT)
        self.node.attach(self)

        # run task daemon in the background
        asyncio.create_task(self.node.serve_upstream())

        return inputs

    async def run(self, **inputs) -> Any:
        # left for compability.
        # remove later
        return await self.plan(**inputs)

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
    ) -> Task:
        """
        Spawn a child task.

        Arguments:
            name (str): Task name
            image (str): Task image. Defaults to parent image.
            kwargs (dict): Input arguments
        """

        # await any inputs
        for key, value in inputs.items():
            if isinstance(value, TaskDefinition):
                inputs[key] = await value.result

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

        # attach a future
        task.result = asyncio.Future()

        self.tasks[task.id] = task
        return task

    @abstractmethod
    async def plan(self, **inputs):
        """ Virtual method for scheduling subtasks """
        return None
