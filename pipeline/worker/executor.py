import asyncio
import traceback
from pipeline.engine import ClusterProvider
from pipeline.network import ConnectionClosedOK, ConnectionClosedError
from pipeline.tasks import TaskDefinition
from .worker_node import WorkerNode
from .service import FlowLogger, NopLogger


async def execute(cluster: ClusterProvider, taskdef: TaskDefinition) -> None:
    """
    Executes a task on this worker node.
    """

    # create network node
    node = WorkerNode(cluster, taskdef)

    if taskdef.upstream:
        if taskdef.upstream == 'disabled':
            node.parent = NopLogger()
        else:
            print('~~ connecting upstream')

            # handle downstream messages
            node.io.create_task(node.parent.serve(taskdef.upstream))

            while node.parent.ws is None:
                await asyncio.sleep(0.1)
    else:
        # if we dont have anywhere to forward events, log them to stdout.
        # logs will be picked up from the top level task by docker/kubernetes.
        node.parent = FlowLogger()

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
        # ensure event loop has a chance to run
        await asyncio.sleep(0.5)

        await node.close()
