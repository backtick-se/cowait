import asyncio
from typing import Any
from abc import abstractmethod
from concurrent.futures import Future
from pipeline.tasks import Task, TaskDefinition, TaskError
from pipeline.network import get_local_connstr


class Flow(Task):
    """ Serves as the base class for all tasks with children """

    async def before(self, inputs: dict) -> None:
        self.tasks = {}

        # subscribe to child task status updates
        self.node.children.on('return', self.on_child_return)
        self.node.children.on('fail', self.on_child_fail)

        # forward child events to parent
        async def forward(conn, **msg):
            await self.node.parent.send(msg)
        self.node.children.on('*', forward)

        # run task daemon in the background
        self.node.io.create_task(self.node.children.serve())

        return inputs

    @abstractmethod
    async def run(self, **inputs: dict) -> Any:
        """ Virtual method for scheduling subtasks """
        return None

    def stop(self) -> None:
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
        ports: dict = {},
        env: dict = {},
        **inputs: dict,
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
                inputs[key] = await asyncio.wrap_future(value.result)

        taskdef = TaskDefinition(
            name=name,
            inputs=inputs,
            parent=self.id,
            image=image if image else self.image,
            upstream=get_local_connstr(),
            config=self.config,
            ports=ports,
            env={
                **self.env,
                **env,
            },
        )

        task = self.cluster.spawn(taskdef)

        # attach a future
        task.result = Future()

        self.tasks[task.id] = task
        return task

    async def on_child_return(self, conn, id: str, result: Any, **msg: dict) -> None:
        task = self.tasks[id]
        if not task.result.done():
            task.result.set_result(result)

    async def on_child_fail(self, conn, id: str, error: str, **msg: dict) -> None:
        task = self.tasks[id]
        if not task.result.done():
            task.result.set_exception(TaskError(error))
