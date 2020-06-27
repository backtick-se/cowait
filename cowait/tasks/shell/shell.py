import os
import asyncio
from cowait.tasks import Task, rpc
from cowait.types import Dict

ShellResult = Dict({
    'code': int,
})


class ShellTask(Task):
    async def run(self, command: str, env: dict = {}) -> ShellResult:
        # run shell command
        self.process = await asyncio.create_subprocess_shell(
            command,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            env={
                **os.environ,
                **env,
            }
        )

        # setup stream readers
        print_stream(self.process.stdout, 'stdout', self.filter_stdout)
        print_stream(self.process.stderr, 'stderr', self.filter_stderr)

        # wait for process to finish
        result = await self.process.wait()

        return {
            'code': result,
        }

    def filter_stdout(self, line: str) -> bool:
        return True

    def filter_stderr(self, line: str) -> bool:
        return True

    @rpc
    async def stop(self):
        print('Stopping shell process')
        self.process.kill()
        return await super().stop()


def print_stream(stream, name: str, filter: callable) -> None:
    async def logger() -> None:
        while True:
            line = await stream.readline()
            if line == b'':
                return

            text = line.decode('utf-8')
            if filter is not None:
                if not filter(text):
                    continue

            print(text, end='')

    asyncio.create_task(logger())
