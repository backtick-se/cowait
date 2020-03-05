import asyncio
import traceback
from pipeline.engine import ClusterProvider
from pipeline.tasks import TaskDefinition
from .worker_node import WorkerNode
from .service import FlowLogger, NopLogger


async def execute(cluster: ClusterProvider, taskdef: TaskDefinition) -> None:
    """
    Executes a task on this worker node.
    """

    # create network node
    node = WorkerNode(taskdef.id)

    if taskdef.upstream:
        if taskdef.upstream == 'disabled':
            node.parent = NopLogger(taskdef.id)
        else:
            # start upstream client
            await node.connect(taskdef.upstream)
    else:
        # if we dont have anywhere to forward events, log them to stdout.
        # logs will be picked up from the top level task by docker/kubernetes.
        print('~~ output logging enabled')
        node.parent = FlowLogger(taskdef.id)

    try:
        # run task
        await node.run(taskdef, cluster)

    except Exception as e:
        # capture local errors
        error = traceback.format_exc()
        await node.parent.send_fail(
            f'Caught exception in {taskdef.id}:\n'
            f'{error}')
        raise e

    finally:
        await node.close()

        # ensure event loop has a chance to run
        await asyncio.sleep(0.5)
