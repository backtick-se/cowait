import asyncio
from typing import Any
from abc import abstractmethod
from pipeline.tasks import Task, TaskDefinition, TaskError
from pipeline.network import get_local_connstr


class Flow(Task):
    """ Serves as the base class for all tasks with children """

    async def before(self, inputs: dict) -> None:
        self.tasks = {}
        self.conns = {}

        # subscribe to child task status updates
        self.node.children.on('init', self.on_child_init)
        self.node.children.on('return', self.on_child_return)
        self.node.children.on('fail', self.on_child_fail)
        self.node.children.on('error', self.on_child_error)

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

    def task(
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

        if not isinstance(name, str) and issubclass(name, Task):
            name = name.__module__

        # todo: throw error if any input is a coroutine

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

        # set up init timeout check
        self.set_init_timeout(task, 30)

        self.tasks[task.id] = task
        return task

    def set_init_timeout(self, task, timeout):
        async def timeout_check(task, timeout):
            await asyncio.sleep(timeout)
            if not task.future.done() and task.id not in self.conns.values():
                task.future.set_exception(TaskError(
                    f'{task.id} timed out before initialization'))

        self.node.io.create_task(timeout_check(task, timeout))

    async def on_child_init(self, conn, id: str, task: dict, **msg: dict):
        if conn not in self.conns:
            self.conns[conn] = id

    async def on_child_return(self, conn, id: str, result: Any, **msg: dict):
        task = self.tasks[id]
        if not task.future.done():
            task.future.set_result(result)

    async def on_child_fail(self, conn, id: str, error: str, **msg: dict):
        task = self.tasks[id]
        if not task.future.done():
            task.future.set_exception(TaskError(error))

    async def on_child_error(self, conn, reason: str):
        if conn in self.conns:
            task_id = self.conns[conn]
            task = self.tasks[task_id]
            if not task.future.done():
                task.future.set_exception(TaskError(
                    f'Lost connection to {task_id}'))
