import os
import asyncio
from pipeline.tasks import Task


class ShellTask(Task):
    async def run(self, command, **inputs):
        # run shell command
        process = await asyncio.create_subprocess_shell(
            command,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            env=os.environ,  # inherit environment
        )

        # setup stream readers
        stream_log_to_node(process.stdout, self.node, 'stdout')
        stream_log_to_node(process.stderr, self.node, 'stderr')

        # wait for process to finish
        result = await process.wait()

        return {
            'code': result,
        }


def stream_log_to_node(stream, node, name):
    async def logger():
        while True:
            line = await stream.readline()
            if line == b'':
                return

            await node.parent.send_log(name, line.decode('utf-8'))

    asyncio.create_task(logger())
