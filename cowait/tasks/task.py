import sys
import inspect
from typing import Any
from cowait.types import serialize
from .definition import TaskDefinition
from .components import TaskManager, RpcComponent, rpc
from .parent_task import ParentTask


class Task(object):
    __current__ = None

    def __init__(self, **inputs):
        """
        Creates a new instance of the task. Pass inputs as keyword arguments.
        """

        # We are using **inputs keyword arguments so that in-IDE tooltips will be more helpful
        # (at least less confusing) when invoking subtasks using constructor syntax.
        # However, subtasks will actually never be instantiated. The constructor call is
        # diverted by the runtime in Task.__new__().
        # Tasks should only be constructed by the executor, and it will these 3 arguments:
        if 'taskdef' not in inputs or 'node' not in inputs or \
           'cluster' not in inputs or len(inputs) != 3:
            raise RuntimeError('Invalid task class instantiation')

        self.node = inputs['node']
        self.cluster = inputs['cluster']
        self.taskdef = inputs['taskdef']

        self.parent = ParentTask(self.node)
        self.subtasks = TaskManager(self)
        self.rpc = RpcComponent(self)

        # Set this task as the current active task
        Task.set_current(self)

    def __new__(cls, *args, **inputs):
        current = Task.get_current()
        if current is None:
            # There is no active task. Continue normal instantiation.
            return object.__new__(cls)
        else:
            # There is already an active task in this process, so we should spawn a subtask.
            # Divert constructor behaviour to instead spawn a remote task and return it.

            if len(args) > 0:
                raise TypeError('Tasks do not accept positional arguments')

            return current.spawn(cls, inputs=inputs)

    @property
    def id(self) -> str:
        return self.taskdef.id

    @property
    def image(self) -> str:
        return self.taskdef.image

    @property
    def meta(self) -> dict:
        return self.taskdef.meta

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

        # send a stop status
        await self.node.parent.send_stop()

        # stop subtasks
        for task in self.subtasks.values():
            await task.stop()

        # schedule exit on the next event loop.
        # allows the RPC call to return before exit.
        async def _quit():
            sys.exit(1)
        self.node.io.create_task(_quit())

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
        volumes: dict = {},
        cpu: str = None,
        cpu_limit: str = None,
        memory: str = None,
        memory_limit: str = None,
        affinity: str = None,
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

        # merge inputs with remaining kwargs
        inputs = {
            **inputs,
            **kwargs,
        }

        if isinstance(name, str):
            pass
        elif issubclass(name, Task):
            name = name.__module__
        else:
            raise TypeError('Unsupported task type: ' + type(name))

        # throw error if any input is a coroutine
        for key, value in inputs.items():
            if inspect.iscoroutine(value):
                raise TypeError(f'Input {key} must be awaited first')

        taskdef = TaskDefinition(
            id=id,
            name=name,
            parent=self.id,
            image=image if image else self.image,
            upstream=self.node.get_url(),
            meta=meta,
            ports=ports,
            routes=routes,
            cpu=cpu if cpu else self.taskdef.cpu,
            cpu_limit=cpu_limit if cpu_limit else self.taskdef.cpu_limit,
            memory=memory if memory else self.taskdef.memory,
            memory_limit=memory_limit if memory_limit else self.taskdef.memory_limit,
            affinity=affinity if affinity else self.taskdef.affinity,
            owner=owner,
            inputs=serialize(inputs),
            storage=self.taskdef.storage,
            volumes={
                **self.taskdef.volumes,
                **volumes,
            },
            env={
                **self.taskdef.env,
                **env,
            },
        )

        # authorize id
        self.node.server.auth.add_token(taskdef.id)

        # spawn task
        task = self.cluster.spawn(taskdef)

        # register with subtask manager
        self.subtasks.watch(task)

        return task

    @staticmethod
    def get_current() -> 'Task':
        return Task.__current__

    @staticmethod
    def set_current(task: 'Task'):
        Task.__current__ = task
