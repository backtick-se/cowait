import asyncio
from typing import Any
from cowait.network import ON_CLOSE
from cowait.utils import Version
from ..status import WAIT, WORK, FAIL
from ..messages import TASK_INIT, TASK_STATUS, TASK_FAIL, TASK_RETURN
from ..instance import TaskInstance
from ..remote_task import RemoteTask


class TaskManager(dict):
    """ Keeps track of the state of subtasks """

    def __init__(self, task):
        self.task = task
        self.conns = {}

        # subscribe to child task status updates
        task.node.server.on(TASK_INIT, self.on_child_init)
        task.node.server.on(TASK_STATUS, self.on_child_status)
        task.node.server.on(TASK_RETURN, self.on_child_return)
        task.node.server.on(TASK_FAIL, self.on_child_fail)
        task.node.server.on(ON_CLOSE, self.on_child_close)

        # forward child events to parent
        async def forward(conn, **msg):
            if msg.get('type', '__')[:2] == '__':
                return
            await task.node.parent.send(msg)
        task.node.server.on('*', forward)

    def watch(self, task, timeout=30):
        # set up init timeout check
        self.set_init_timeout(task, timeout)
        self[task.id] = task

    def set_init_timeout(self, task, timeout):
        async def timeout_check(task, timeout):
            await asyncio.sleep(timeout)
            if not task.future.done() and task.id not in self.conns.values():
                await self.emit_child_error(
                    id=task.id, error=f'{task.id} timed out before initialization')

        self.task.node.io.create_task(timeout_check(task, timeout))

    async def on_child_init(self, conn, id: str, task: dict, version: str, **msg: dict):
        # version check
        try:
            version = Version.parse(version)
            if not version.is_compatible():
                raise RuntimeError(f'{id} runs an incompatible library version: {version}')
        except Exception as e:
            await self.emit_child_error(id=task.id, error=str(e))
            await conn.close()
            if conn in self.conns:
                del self.conns[conn]
            if id in self:
                del self[id]
            return

        # register connection if its not yet known
        if conn not in self.conns:
            self.conns[conn] = id

        if id in self:
            # we have seen this task before. thats strange and might indicate an error.
            # set task connection reference
            task = self[id]
            task.conn = conn
        else:
            # this task is not known - its either a virtual task or a child of a child.
            # check if it has the running task set as its parent, if so, try to adopt it.
            taskdef = TaskInstance.deserialize(task)
            if taskdef.parent != self.task.id:
                return

            task = RemoteTask(taskdef, self.task.cluster)
            task.conn = conn
            self[id] = task

    async def on_child_status(self, conn, id: str, status: str, **msg: dict):
        if id in self:
            task = self[id]
            task.set_status(status)

    async def on_child_return(self, conn, id: str, result: Any, result_type: any, **msg: dict):
        if id in self:
            task = self[id]
            task.set_result(result, result_type)

    async def on_child_fail(self, conn, id: str, error: str, **msg: dict):
        if id in self:
            task = self[id]
            task.set_error(error)

    async def on_child_close(self, conn, **msg: dict) -> None:
        if conn not in self.conns:
            return

        # lookup task & remove from active connections
        task_id = self.conns[conn]
        task = self[task_id]
        del self.conns[conn]

        # unset task connection reference
        task.conn = None

        # emit an error event if connection was lost before done/fail
        if task.status == WAIT or task.status == WORK:
            await self.emit_child_error(
                conn=conn, id=task.id, error=f'Lost connection to {task_id}')

    async def emit_child_error(self, id, error, conn=None):
        await self.task.node.server.emit(type=TASK_STATUS, id=id, status=FAIL, conn=conn)
        await self.task.node.server.emit(type=TASK_FAIL, id=id, conn=conn, error=error)
