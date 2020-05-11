import asyncio
import traceback
from cowait.engine import ClusterProvider
from cowait.tasks import TaskDefinition, TaskError
from cowait.types import typed_arguments, typed_return
from .worker_node import WorkerNode
from .service import FlowLogger, NopLogger
from .loader import load_task_class


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
        node.parent = FlowLogger(taskdef.id)

    try:
        # init should always be the first command sent
        await node.parent.send_init(taskdef)

        # run task within a log capture context
        with node.capture_logs():
            # instantiate
            TaskClass = load_task_class(taskdef.name)
            task = TaskClass(taskdef, cluster, node)

            # initialize task
            task.init()

            # start http server
            node.io.create_task(node.http.serve())

            # prepare & typecheck inputs
            inputs = typed_arguments(task.run, taskdef.inputs)

            # set state to running
            await node.parent.send_run()

            # before hook
            inputs = await task.before(inputs)
            if inputs is None:
                raise ValueError(
                    'Task.before() returned None, '
                    'did you forget to return inputs?')

            # execute task
            result = await task.run(**inputs)

            # wait for dangling tasks
            orphans = filter(lambda child: not child.done, task.subtasks.values())
            for orphan in orphans:
                print('~~ waiting for orphaned task', orphan.id)
                await orphan

            # after hook
            await task.after(inputs)

            # prepare & typecheck result
            result, result_type = typed_return(task.run, result)

            # submit result
            await node.parent.send_done(result, result_type)

    except TaskError as e:
        # pass subtask errors upstream
        await node.parent.send_fail(
            f'Caught exception in subtask {taskdef.id}:\n'
            f'{e.error}')
        raise e

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
