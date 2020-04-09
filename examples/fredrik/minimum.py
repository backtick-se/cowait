from pipeline.tasks import Task, join

class Minimum(Task):
    async def run(self, value1=1, value2=2, value3=3):
        tasks = join([
            Number(value=value1),
            Number(value=value2),
            Number(value=value3)
        ])

        return min(await tasks)