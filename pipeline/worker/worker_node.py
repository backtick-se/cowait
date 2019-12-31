

import asyncio
from contextlib import nullcontext
from pipeline.network import Node
from pipeline.tasks import TaskError, StopException
from pipeline.utils import StreamCapturing
from .worker_api import WorkerAPI
from .service import FlowLogger
from .loader import load_task_class


class WorkerNode(Node):
    def __init__(self, cluster, taskdef):
        super().__init__()
        self.cluster = cluster
        self.api = WorkerAPI(self, taskdef)

    async def run(self, taskdef):
        try:
            await self.api.init()

            # run task within a log capture context
            with self.capture_logs():
                # todo: perhaps we want to use an external process for this?
                # - easy to capture stdin/stdout
                # - error isolation
                # - language agnosticism!

                # instantiate
                TaskClass = load_task_class(taskdef.name)
                task = TaskClass(taskdef, self.cluster, self)

                # run task
                await self.api.run()

                # before hook - transform input
                inputs = await task.before(taskdef.inputs)

                try:
                    # task code
                    result = await task.run(**inputs)

                    # submit result
                    await self.api.done(result)

                finally:
                    # after hook
                    await task.after(inputs)

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

        def stdout(x):
            return asyncio.ensure_future(self.api.log('stdout', x))

        def stderr(x):
            return asyncio.ensure_future(self.api.log('stderr', x))

        return StreamCapturing(stdout, stderr)
