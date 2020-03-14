import sys
import asyncio
from pipeline.tasks import Task


class ShellTask(Task):
    async def run(self, command, **inputs):
        # run shell command
        process = await asyncio.create_subprocess_shell(
            command,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            env=self.env,  # inherit environment
        )

        # setup stream readers
        stream_log_to_node(process.stdout, sys.stdout, self.node, 'stdout')
        stream_log_to_node(process.stderr, sys.stderr, self.node, 'stderr')

        # wait for process to finish
        result = await process.wait()

        return {
            'code': result,
        }


def stream_log_to_node(stream, out_stream, node, name):
    async def logger():
        while True:
            line = await stream.readline()
            if line == b'':
                return

            print(line.decode('utf-8'), file=out_stream, end='', flush=True)

    asyncio.create_task(logger())
