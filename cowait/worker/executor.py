import traceback
from cowait.engine import ClusterProvider
from cowait.tasks import Task, TaskDefinition, TaskError
from cowait.types import typed_arguments, typed_return, get_parameter_defaults
from cowait.storage import StorageBackends
from .worker_node import WorkerNode
from .loader import load_task_class


async def execute(cluster: ClusterProvider, taskdef: TaskDefinition) -> None:
    """
    Executes a task on this worker node.
    """

    # create network node
    node = WorkerNode(taskdef.id, taskdef.upstream)

    # start upstream client
    await node.connect()

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

            # initialize storage
            setattr(task, 'storage', StorageBackends(taskdef.storage))

            # monitor system resources
            node.monitor_system(interval=2)

            # initialize task
            task.init()

            # start http server
            # this must happen after task.init() so that tasks have a chance
            # to register extra http routes.
            node.serve()

            # unpack wrapped function if defined.
            # allows typechecking of functional tasks
            taskfunc = task.run
            if hasattr(TaskClass, '__wraps__'):
                taskfunc = TaskClass.__wraps__

            # prepare arguments
            inputs = {
                **get_parameter_defaults(taskfunc),
                **taskdef.inputs,
            }

            # before hook
            inputs = await task.before(inputs)
            if inputs is None:
                raise ValueError(
                    'Task.before() returned None, '
                    'did you forget to return the inputs?')

            # typecheck arguments
            inputs = typed_arguments(taskfunc, inputs)

            # set state to running
            await node.parent.send_run()

            # execute task
            result = await task.run(**inputs)

            # after hook
            await task.after(inputs)

            # wait for dangling tasks
            await handle_orphans(task)

            # prepare & typecheck result
            result, result_type = typed_return(taskfunc, result)

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

        # clear active task
        Task.set_current(None)


async def handle_orphans(task: Task, mode: str = 'stop') -> None:
    orphans = filter(lambda child: not child.done, task.subtasks.values())
    for orphan in orphans:
        if mode == 'wait':
            print('~~ waiting for orphaned task', orphan.id)
            await orphan
        elif mode == 'stop':
            print('~~ stopping orphaned task', orphan.id)
            await orphan.stop()
        else:
            raise RuntimeError(f'Unknown orphan mode {mode}')
