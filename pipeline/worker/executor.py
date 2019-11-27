import asyncio
import traceback
from contextlib import nullcontext
from pipeline.engine import ClusterProvider
from pipeline.network import Node, ConnectionClosedOK, ConnectionClosedError
from pipeline.tasks import TaskContext, TaskDefinition, TaskError, \
    StopException
from pipeline.utils import StreamCapturing
from .loader import instantiate_task_class
from .worker_node import create_worker_node


async def execute(cluster: ClusterProvider, taskdef: TaskDefinition) -> None:
    # create network node
    node = await create_worker_node(taskdef)

    try:
        # create task context
        context = TaskContext(taskdef, cluster, node)

        # instantiate & run task
        await node.api.init(taskdef)
        await node.api.run()

        # run task within a log capture context
        with capture_logs_to_node(node):
            task = instantiate_task_class(context)
            result = await task.run(**taskdef.inputs)

        # submit result
        await node.api.done(result)

    except StopException:
        await node.api.stop()

    except ConnectionClosedOK:
        print('~~ upstream connection closed.')

    except ConnectionClosedError:
        print('~~ upstream connection error:')
        traceback.print_exc()

    except TaskError as e:
        # pass subtask errors upstream
        await node.api.fail(f'Caught exception in {taskdef.id}:\n{e.error}')
        raise e

    except Exception as e:
        # capture local errors
        error = traceback.format_exc()
        await node.api.fail(f'Caught exception in {taskdef.id}:\n{error}')
        raise e

    finally:
        await node.close()


def capture_logs_to_node(node: Node) -> StreamCapturing:
    return StreamCapturing(
        on_stdout=lambda x: asyncio.ensure_future(node.api.log('stdout', x)),
        on_stderr=lambda x: asyncio.ensure_future(node.api.log('stderr', x)),
    ) if node.upstream else nullcontext()
