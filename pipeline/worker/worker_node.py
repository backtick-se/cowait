

from typing import Any
from pipeline.network import Node
from pipeline.tasks import TaskDefinition, WAIT, WORK, DONE, STOP, FAIL
from pipeline.network.service import FlowLogger


async def create_worker_node(taskdef: TaskDefinition) -> Node:
    """
    Create a worker node.
    """

    node = WorkerNode(taskdef.id)

    if not taskdef.parent:
        # set up root node
        if taskdef.upstream:
            # this is the root task but an upstream has been specified.
            # connect upstream and forward events.
            print('~~ root: connecting upstream')
            node.connect(taskdef.upstream)
        else:
            # if we dont have anywhere to forward events, log them to stdout. 
            # logs will be picked up by docker/kubernetes.
            node.attach(FlowLogger())

    else:
        # set up child node
        # connect upstream and forward events.
        print('~~ child: connecting upstream')
        await node.connect(taskdef.upstream)

    return node


class WorkerNode(Node):
    """
    Extends a network node with Worker specific API functionality.
    """

    async def send_msg(self, type: str, **msg):
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

    
    async def send_init(self, taskdef) -> None:
        """
        Send a task initialization message.

        Arguments:
            taskdef (TaskDefinition): New task definition
        """
        await self.send_msg('init', task=taskdef.serialize())


    async def send_run(self) -> None:
        """ Send status update: Running """
        await self.send_msg('status', status=WORK)


    async def send_stop(self, id=None) -> None:
        """ Send status update: Stopped """
        await self.send_msg('status', status=STOP, id=id)
        await self.send_msg('return', result={}, id=id)


    async def send_done(self, result: Any) -> None:
        """ 
        Send status update: Done, and return a result.

        Arguments:
            result (any): Any json-serializable data to return to the upstream task.
        """
        await self.send_msg('status', status=DONE)
        await self.send_msg('return', result=result)


    async def send_fail(self, error: str) -> None:
        """
        Send an error.

        Arguments:
            error (str): Error message
        """
        await self.send_msg('status', status=FAIL)
        await self.send_msg('fail',   error=error)


    async def send_log(self, file: str, data: str) -> None:
        """
        Send captured log output.

        Arguments:
            file (str): Capture source (stdout/stderr)
            data (str): Captured output data
        """
        await self.send_msg('log', file=file, data=data)
