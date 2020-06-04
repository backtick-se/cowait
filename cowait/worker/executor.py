import asyncio
import traceback
from cowait.engine import ClusterProvider
from cowait.tasks import Task, TaskDefinition, TaskError
from cowait.types import typed_arguments, typed_return, get_return_type, get_parameter_defaults
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
            task = TaskClass(
                taskdef=taskdef,
                cluster=cluster,
                node=node,
            )

            # initialize task
            task.init()

            # start http server
            node.io.create_task(node.http.serve())

            # prepare arguments
            inputs = {
                **get_parameter_defaults(task.run),
                **taskdef.inputs,
            }

            # before hook
            inputs = await task.before(inputs)
            if inputs is None:
                raise ValueError(
                    'Task.before() returned None, '
                    'did you forget to return the inputs?')

            # typecheck arguments
            inputs = typed_arguments(task.run, inputs)

            # set state to running
            await node.parent.send_run()

            # execute task
            result = await task.run(**inputs)

            # after hook
            await task.after(inputs)

            # wait for dangling tasks
            await handle_orphans(task)

            # prepare & typecheck result
            result = typed_return(task.run, result)
            result_type = get_return_type(task.run)

            # submit result
            await node.parent.send_done(result, result_type.describe())

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


async def handle_orphans(task: Task, mode: str = 'kill') -> None:
    orphans = filter(lambda child: not child.done, task.subtasks.values())
    for orphan in orphans:
        if mode == 'wait':
            print('~~ waiting for orphaned task', orphan.id)
            await orphan
        elif mode == 'kill':
            print('~~ killing orphaned task', orphan.id)
            orphan.destroy()
        else:
            raise RuntimeError(f'Unknown orphan mode {mode}')
