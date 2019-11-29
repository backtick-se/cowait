import asyncio
from pipeline.tasks import Task


class ShellTask(Task):
    async def run(self, command):
        process = await asyncio.create_subprocess_shell(
            command,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
        )

        def decode(s): return s.decode('utf-8')
        out, err = map(decode, await process.communicate())

        return {
            'out': out,
            'err': err,
        }
