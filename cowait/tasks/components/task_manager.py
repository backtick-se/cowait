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
        # maybe move it out?
        task.node.server.on(TASK_INIT, self.on_child_init)
        task.node.server.on(TASK_STATUS, self.on_child_status)
        task.node.server.on(TASK_RETURN, self.on_child_return)
        task.node.server.on(TASK_FAIL, self.on_child_fail)
        task.node.server.on(ON_CLOSE, self.on_child_close)

        # forward child events to parent
        # this probably belongs somewhere else...
        async def forward(conn, **msg):
            if msg.get('type', '__')[:2] == '__':
                return
            await task.node.parent.send(msg)
        task.node.server.on('*', forward)

    def watch(self, task, timeout=30):
        """
        Watch for a newly created task. Registers it with the task manager and sets up an
        initialization timeout check.
        """
        self[task.id] = task
        self.task.node.io.create_task(self._init_timeout_check(task, timeout))

    async def _init_timeout_check(self, task, timeout):
        await task.wait_for_scheduling()
        await asyncio.sleep(timeout)
        if not task.future.done() and task.id not in self.conns.values():
            # make sure this task is killed and cant connect after the failure
            # note: there is a race condition here.
            # the kill command might arrive after the error has been sent
            # perhaps we should note that this task has failed, and ignore any
            # further communication from it?
            self.task.cluster.destroy(task.id)

            # emit a timeout error
            await self.emit_child_error(
                id=task.id, error=f'{task.id} timed out before initialization')

    async def on_child_init(self, conn, id: str, task: dict, version: str, **msg: dict):
        # version check
        try:
            version = Version.parse(version)
            if not version.is_compatible():
                raise ValueError(f'{id} runs an incompatible library version: {version}')

        except ValueError as e:
            # illegal version string or incompatible version
            await self.reject(id, str(e), conn)
            return

        # register child task
        self.register(conn, id, task)

    async def reject(self, id, reason: str, conn=None):
        await self.emit_child_error(id=id, error=reason)
        if id in self:
            del self[id]
        if conn is not None:
            await conn.close()
            if conn in self.conns:
                del self.conns[conn]

    def register(self, conn, id, task: dict):
        # register connection if its not yet known
        if conn not in self.conns:
            self.conns[conn] = id

        if id in self:
            # we know about the task - this should mean that its a child of the current task.
            # if not, something weird is going on.
            task = self[id]
            task.conn = conn
        else:
            # this task is not yet known - its either a virtual task or a child of a child.
            # check if it has the running task set as its parent, if so, try to adopt it.
            taskdef = TaskInstance.deserialize(task)
            if taskdef.parent == self.task.id:
                # its a virtual task
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
