
from typing import Any
from pipeline.network import Node
from pipeline.tasks import TaskDefinition, WORK, DONE, STOP, FAIL


class WorkerAPI:
    """
    Upstream API client.
    """

    def __init__(self, node: Node, taskdef: TaskDefinition):
        self.taskdef = taskdef
        self.node = node
        self.id = taskdef.id

    async def send(self, msg: dict) -> None:
        await self.node.send(msg)

    async def msg(self, type: str, **msg) -> None:
        """
        Send a message upstream.

        Arguments:
            type (str): Message type
            kwargs (dict): Message fields
        """
        await self.send({
            'id': self.id,
            'type': type,
            **msg,
        })

    async def init(self) -> None:
        """
        Send a task initialization message.

        Arguments:
            taskdef (TaskDefinition): New task definition
        """
        await self.msg('init', task=self.taskdef.serialize())

    async def run(self) -> None:
        """ Send status update: Running """
        await self.msg('status', status=WORK)

    async def stop(self, id: str = None) -> None:
        """ Send status update: Stopped """
        await self.msg('status', status=STOP, id=id)
        await self.msg('return', result={}, id=id)

    async def done(self, result: Any) -> None:
        """
        Send status update: Done, and return a result.

        Arguments:
            result (any): Any serializable data to return to the upstream task.
        """
        await self.msg('status', status=DONE)
        await self.msg('return', result=result)

    async def fail(self, error: str) -> None:
        """
        Send an error.

        Arguments:
            error (str): Error message
        """
        await self.msg('status', status=FAIL)
        await self.msg('fail',   error=error)

    async def log(self, file: str, data: str) -> None:
        """
        Send captured log output.

        Arguments:
            file (str): Capture source (stdout/stderr)
            data (str): Captured output data
        """
        await self.msg('log', file=file, data=data)
