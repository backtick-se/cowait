import asyncio
import traceback
from contextlib import nullcontext
from pipeline.network import Node
from pipeline.engine import ClusterProvider
from pipeline.tasks import TaskContext, TaskDefinition, TaskError, StopException
from pipeline.utils import StreamCapturing
from .loader import instantiate_task_class
from .worker_node import create_worker_node

import websockets


async def execute(cluster: ClusterProvider, taskdef: TaskDefinition) -> None:
    # create network node
    node = await create_worker_node(taskdef)

    try:
        # create task context
        context = TaskContext(taskdef, cluster, node)

        # instantiate & run task
        await node.send_init(taskdef)
        await node.send_run()

        # run task within a log capture context
        with capture_logs_to_node(node):
            task = instantiate_task_class(context)
            result = await task.run(**taskdef.inputs)

        # submit result
        await node.send_done(result)

    except StopException:
        await node.send_stop()

    except websockets.exceptions.ConnectionClosedOK:
        print('connection closed')

    except websockets.exceptions.ConnectionClosedError:
        print('connection error')

    except TaskError as e:
        # pass subtask errors upstream
        await node.send_fail(f'Caught exception in task {taskdef.id}:\n{e.error}')
        raise e

    except Exception as e:
        # capture local errors
        error = traceback.format_exc()
        await node.send_fail(f'Caught exception in task {taskdef.id}:\n{error}')
        raise e

    finally:
        await node.close()


def capture_logs_to_node(node):
    return StreamCapturing(
        on_stdout = lambda x: asyncio.ensure_future(node.send_log('stdout', x)),
        on_stderr = lambda x: asyncio.ensure_future(node.send_log('stderr', x)),
    ) if node.upstream else nullcontext()
