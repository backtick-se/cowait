from random import randint
from cowait.worker.worker_node import WorkerNode
from .html_logger import HTMLLogger


class NotebookNode(WorkerNode):
    """
    The Notebook Node is a variant of the standard worker node meant to run in a notebook.
    It simulates a running task by connecting upstream and forwarding events from tasks
    created from within the notebook.

    NotebookNodes use random ports for their web servers to allow multiple nodes on a single host.
    Output is disabled to prevent event spam into the notebook.
    """

    def __init__(self, taskdef):
        self.taskdef = taskdef
        super().__init__(
            id=taskdef.id,
            upstream=taskdef.upstream,
            port=randint(10000, 60000),
            logger=HTMLLogger(),
        )

    async def start(self, token: str) -> None:
        """
        Starts the node by connecting upstream, sending initialization
        events and starting the local web server.
        """
        await self.connect(token)
        await self.parent.send_init(self.taskdef)
        await self.parent.send_run()
        await self.parent.send_log(data='Kernel ready.', file='stdout')
        self.serve()

    async def stop(self):
        await self.parent.send_log(data='Kernel stopped!', file='stdout')
        await self.parent.send_stop()
        await self.parent.close()

    async def connect(self, token: str) -> None:
        await self.parent.connect(self.upstream, token)
