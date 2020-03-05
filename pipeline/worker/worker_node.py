import asyncio
from contextlib import nullcontext
from pipeline.network import Server, HttpServer
from pipeline.tasks import TaskError, StopException
from pipeline.utils import StreamCapturing
from .service import FlowLogger
from .io_thread import IOThread
from .loader import load_task_class
from .parent_client import ParentClient


class WorkerNode(object):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.io = IOThread()
        self.io.start()

        self.http = HttpServer()
        self.children = Server(self)
        self.parent = ParentClient(id)

    async def connect(self, uri) -> None:
        self.io.create_task(self.parent.connect(uri, self.id))
        while not self.parent.connected:
            await asyncio.sleep(0.1)

    async def close(self) -> None:
        async def close():
            if self.children:
                await self.children.close()
            if self.parent:
                await self.parent.close()

        await self.io.create_task(close())

    async def run(self, taskdef, cluster):
        try:
            await self.parent.send_init(taskdef)

            # run task within a log capture context
            with self.capture_logs():
                # instantiate
                TaskClass = load_task_class(taskdef.name)
                task = TaskClass(taskdef, cluster, self)

                # initialize task
                task.init()

                # start http server
                self.io.create_task(self.http.serve())

                # set state to running
                await self.parent.send_run()

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
                await self.parent.send_done(result)

        except StopException:
            await self.parent.send_stop()

        except TaskError as e:
            # pass subtask errors upstream
            await self.parent.send_fail(
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
                self.io.create_task(self.parent.send_log(file, x))
            return callback

        return StreamCapturing(logger('stdout'), logger('stderr'))
