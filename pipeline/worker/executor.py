import asyncio
import traceback
from contextlib import nullcontext
from pipeline.network import Node
from pipeline.engine import ClusterProvider
from pipeline.tasks import TaskContext, TaskDefinition, TaskError, StopException
from pipeline.utils import StreamCapturing
from .loader import instantiate_task_class


async def execute(cluster: ClusterProvider, node: Node, taskdef: TaskDefinition) -> None:
    try:
        # create task context
        context = TaskContext(
            cluster = cluster,
            taskdef = taskdef,
            node    = node,
        )

        # instantiate & run task
        node.send_init(taskdef)
        node.send_run()

        # run task within a log capture context
        with capture_logs_to_node(node):
            task = instantiate_task_class(context)
            result = await task.run(**taskdef.inputs)

        # submit result
        node.send_done(result)

    except StopException:
        node.send_stop()

    except TaskError as e:
        # pass subtask errors upstream
        traceback.print_exc()
        node.send_fail(e.error)
        exit(1)

    except:
        # capture local errors
        print('CAUGHT EXCEPTION:')
        traceback.print_exc()

        error = traceback.format_exc()
        node.send_fail(error)
        exit(1)

    finally:
        # clean exit
        exit(0)


def capture_logs_to_node(node):
    return StreamCapturing(
        on_stdout = lambda x: node.send_log('stdout', x),
        on_stderr = lambda x: node.send_log('stderr', x),
    ) if node.upstream else nullcontext()
