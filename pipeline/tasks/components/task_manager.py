import asyncio
from typing import Any
from ..errors import TaskError


class TaskManager(object):
    """ Keeps track of the state of subtasks """

    def __init__(self, task):
        self.task = task
        self.tasks = {}
        self.conns = {}

        # subscribe to child task status updates
        task.node.children.on('init', self.on_child_init)
        task.node.children.on('return', self.on_child_return)
        task.node.children.on('fail', self.on_child_fail)
        task.node.children.on('error', self.on_child_error)

        # forward child events to parent
        async def forward(conn, **msg):
            await task.node.parent.send(msg)
        task.node.children.on('*', forward)

    def __getitem__(self, task_id):
        return self.tasks[task_id]

    def watch(self, task):
        # set up init timeout check
        self.set_init_timeout(task, 30)
        self.tasks[task.id] = task

    def set_init_timeout(self, task, timeout):
        async def timeout_check(task, timeout):
            await asyncio.sleep(timeout)
            if not task.future.done() and task.id not in self.conns.values():
                task.future.set_exception(TaskError(
                    f'{task.id} timed out before initialization'))

        self.task.node.io.create_task(timeout_check(task, timeout))

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
