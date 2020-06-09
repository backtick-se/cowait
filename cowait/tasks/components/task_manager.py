import asyncio
from typing import Any
from ..errors import TaskError
from ..messages import TASK_INIT, TASK_STATUS, TASK_FAIL, TASK_RETURN


class TaskManager(dict):
    """ Keeps track of the state of subtasks """

    def __init__(self, task):
        self.task = task
        self.conns = {}

        # subscribe to child task status updates
        task.node.children.on(TASK_INIT, self.on_child_init)
        task.node.children.on(TASK_STATUS, self.on_child_status)
        task.node.children.on(TASK_RETURN, self.on_child_return)
        task.node.children.on(TASK_FAIL, self.on_child_fail)
        task.node.children.on('error', self.on_child_error)

        # forward child events to parent
        async def forward(conn, **msg):
            await task.node.parent.send(msg)
        task.node.children.on('*', forward)

    def watch(self, task):
        # set up init timeout check
        self.set_init_timeout(task, 30)
        self[task.id] = task

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

        if id in self:
            task = self[id]
            task.conn = conn

    async def on_child_status(self, conn, id: str, status: str, **msg: dict):
        if id in self:
            task = self[id]
            task.set_status(status)

    async def on_child_return(self, conn, id: str, result: Any, result_type: any, **msg: dict):
        task = self[id]
        task.set_result(result, result_type)

    async def on_child_fail(self, conn, id: str, error: str, **msg: dict):
        task = self[id]
        task.set_error(error)

    async def on_child_error(self, conn, reason: str):
        if conn in self.conns:
            task_id = self.conns[conn]
            task = self[task_id]
            task.set_error(f'Lost connection to {task_id}')
