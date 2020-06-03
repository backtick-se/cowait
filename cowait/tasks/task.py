import os
from typing import Any
from cowait.network import get_local_connstr
from .definition import TaskDefinition
from .components import TaskManager, RpcComponent, rpc


CURRENT_TASK = None


class Task(TaskDefinition):
    def __init__(
        self,
        **inputs,
    ):
        """
        Creates a new instance of the task. Pass inputs as keyword arguments.
        """
        # we are using **inputs keyword arguments so that the documentation will be
        # more helpful when invoking subtasks.
        kwargs = inputs['taskdef'].serialize()
        super().__init__(**kwargs)
        self.node = inputs['node']
        self.cluster = inputs['cluster']
        self.subtasks = TaskManager(self)
        self.rpc = RpcComponent(self)

        # the base task constructor only takes 3 arguments.
        if len(inputs) != 3:
            raise RuntimeError('Invalid task constructor call')

    def __new__(cls, *args, **inputs):
        global CURRENT_TASK
        if CURRENT_TASK is None:
            # there is no active task.
            # instantiate one and make it the active task.
            task = object.__new__(cls)
            CURRENT_TASK = task
            return task
        else:
            # we already have a task.
            # spawn a remote task and return it.

            if len(args) > 0:
                raise RuntimeError('Tasks do not accept positional arguments')

            return CURRENT_TASK.spawn(cls, **inputs)

    def __str__(self) -> str:
        return f'Task({self.id}, {self.name})'

    def init(self):
        pass

    async def before(self, inputs: dict) -> dict:
        return inputs

    async def run(self, **inputs: dict) -> Any:
        pass

    async def after(self, inputs: dict) -> Any:
        pass

    @rpc
    async def stop(self) -> None:
        """
        Abort task execution.
        """
        print('\n~~ STOPPED ~~')

        await self.node.parent.send_stop()
        for task in self.subtasks.values():
            await task.stop()

        os._exit(1)

    def spawn(
        self,
        name: str,
        id: str = None,
        image: str = None,
        ports: dict = {},
        routes: dict = {},
        inputs: dict = {},
        meta: dict = {},
        env: dict = {},
        cpu: str = '0',
        memory: str = '0',
        owner: str = '',
        **kwargs: dict,
    ) -> 'Task':
        """
        Spawn a subtask.

        Arguments:
            name (str): Task name
            image (str): Task image. Defaults to the current task image.
            kwargs (dict): Input arguments
        """

        if not isinstance(name, str) and issubclass(name, Task):
            name = name.__module__

        # todo: throw error if any input is a coroutine

        taskdef = TaskDefinition(
            id=id,
            name=name,
            parent=self.id,
            image=image if image else self.image,
            upstream=get_local_connstr(),
            meta=meta,
            ports=ports,
            routes=routes,
            cpu=cpu,
            memory=memory,
            owner=owner,
            inputs={
                **inputs,
                **kwargs,
            },
            env={
                **self.env,
                **env,
            },
        )

        # authorize id
        self.node.http.auth.add_token(taskdef.id)

        # spawn task
        task = self.cluster.spawn(taskdef)

        # register with subtask manager
        self.subtasks.watch(task)

        return task
