from cowait.tasks.shell import ShellTask


class DaskWorker(ShellTask):
    async def run(self, scheduler: str, **inputs):
        command = f'dask-worker {scheduler}'
        return await super().run(command=command, **inputs)
