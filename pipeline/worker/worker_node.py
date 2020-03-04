from contextlib import nullcontext
from pipeline.network import Node
from pipeline.tasks import TaskError, StopException
from pipeline.utils import StreamCapturing
from .worker_api import WorkerAPI
from .service import FlowLogger
from .io_thread import IOThread
from .loader import load_task_class


class WorkerNode(Node):
    def __init__(self, cluster, taskdef):
        super().__init__()
        self.cluster = cluster
        self.api = WorkerAPI(self, taskdef)
        self.io = IOThread()
        self.io.start()

        self.io.create_task(self.children.serve())

    async def run(self, taskdef):
        try:
            await self.api.init()

            # run task within a log capture context
            with self.capture_logs():
                # instantiate
                TaskClass = load_task_class(taskdef.name)
                task = TaskClass(taskdef, self.cluster, self)

                # set state to running
                await self.api.run()

                # before hook
                inputs = await task.before(taskdef.inputs)
                if inputs is None:
                    raise ValueError(
                        'Task.before() returned None, '
                        'did you forget to return inputs?')

                # execute task
                result = await task.run(**inputs)

                # after hook
                await task.after(inputs)

                # submit result
                await self.api.done(result)

        except StopException:
            await self.api.stop()

        except TaskError as e:
            # pass subtask errors upstream
            await self.api.fail(
                f'Caught exception in {taskdef.id}:\n'
                f'{e.error}')

    def capture_logs(self) -> StreamCapturing:
        """ Sets up a stream capturing context, forwarding logs to the node """
        # hack to avoid stdout loop
        if isinstance(self.parent, FlowLogger):
            return nullcontext()

        def logger(file):
            def callback(x):
                nonlocal file
                self.io.create_task(self.api.log(file, x))
            return callback

        return StreamCapturing(logger('stdout'), logger('stderr'))

    async def close(self):
        self.io.create_task(super().close())
