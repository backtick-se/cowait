
from typing import Any
from cowait.network import Client
from cowait.tasks import TaskDefinition, WORK, DONE, STOP, FAIL
from cowait.tasks.messages import \
    TASK_INIT, TASK_LOG, TASK_STATUS, TASK_RETURN, TASK_FAIL


class ParentClient(Client):
    """
    Upstream API client.
    """

    def __init__(self, id: str):
        super().__init__()
        self.id = id

    async def connect(self, url: str, token: str = None) -> None:
        if token is None:
            token = self.id
        return await super().connect(url, token)

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

    async def send_init(self, taskdef: TaskDefinition) -> None:
        """
        Send a task initialization message.

        Arguments:
            taskdef (TaskDefinition): New task definition
        """
        await self.msg(TASK_INIT, task=taskdef.serialize())

    async def send_run(self) -> None:
        """ Send status update: Running """
        await self.msg(TASK_STATUS, status=WORK)

    async def send_stop(self, id: str = None) -> None:
        """ Send status update: Stopped """
        id = self.id if id is None else id
        await self.msg(TASK_STATUS, status=STOP, id=id)
        await self.msg(TASK_RETURN, result={}, id=id)

    async def send_done(self, result: Any, result_type: str = 'any') -> None:
        """
        Send status update: Done, and return a result.

        Arguments:
            result (any): Any serializable data to return to the upstream task.
            result_type (str): Result type description
        """
        await self.msg(TASK_STATUS, status=DONE)
        await self.msg(TASK_RETURN, result=result, result_type=result_type)

    async def send_fail(self, error: str) -> None:
        """
        Send an error.

        Arguments:
            error (str): Error message
        """
        await self.msg(TASK_STATUS, status=FAIL)
        await self.msg(TASK_FAIL,   error=error)

    async def send_log(self, file: str, data: str) -> None:
        """
        Send captured log output.

        Arguments:
            file (str): Capture source (stdout/stderr)
            data (str): Captured output data
        """
        await self.msg(TASK_LOG, file=file, data=data)
