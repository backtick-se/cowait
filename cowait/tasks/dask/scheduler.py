from cowait.tasks.shell import ShellTask


class DaskScheduler(ShellTask):
    async def run(self, **inputs):
        return await super().run(
            command='dask-scheduler',
            **inputs,
        )
