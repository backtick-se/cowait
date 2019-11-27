

from pipeline.network import Node
from pipeline.tasks import TaskDefinition
from .worker_api import WorkerAPI
from .service import FlowLogger


async def create_worker_node(taskdef: TaskDefinition) -> Node:
    """
    Create a worker node.
    """

    node = Node(taskdef.id)
    node.api = WorkerAPI(node)

    if not taskdef.parent:
        # set up root node
        if taskdef.upstream:
            # this is the root task but an upstream has been specified.
            # connect upstream and forward events.
            print('~~ root: connecting upstream')
            await node.connect(taskdef.upstream)
        else:
            # if we dont have anywhere to forward events, log them to stdout.
            # logs will be picked up by docker/kubernetes.
            print('~~ root: stdout mode')
            node.attach(FlowLogger())

    else:
        # set up child node
        # connect upstream and forward events.
        print('~~ child: connecting upstream')
        await node.connect(taskdef.upstream)

    return node
