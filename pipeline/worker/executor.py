import asyncio
import traceback
from pipeline.engine import ClusterProvider
from pipeline.network import ConnectionClosedOK, ConnectionClosedError
from pipeline.tasks import TaskDefinition
from .worker_node import WorkerNode
from .service import FlowLogger


async def execute(cluster: ClusterProvider, taskdef: TaskDefinition) -> None:
    """
    Executes a task on this worker node.
    """

    # create network node
    node = WorkerNode(cluster, taskdef)

    if taskdef.upstream:
        # forward events upstream
        print('~~ connecting upstream')
        await node.connect(taskdef.upstream)

        # handle downstream messages
        asyncio.create_task(node.serve_downstream())
    else:
        # if we dont have anywhere to forward events, log them to stdout.
        # logs will be picked up by docker/kubernetes.
        node.attach(FlowLogger())

    try:
        # run task
        await node.run(taskdef)

    except ConnectionClosedOK:
        print('~~ upstream connection closed')

    except ConnectionClosedError:
        print('~~ upstream connection error')
        traceback.print_exc()

    except Exception as e:
        # capture local errors
        error = traceback.format_exc()
        await node.api.fail(f'Caught exception in {taskdef.id}:\n{error}')
        raise e

    finally:
        await node.close()
