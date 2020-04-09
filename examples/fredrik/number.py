from pipeline.tasks import Task

class Number(Task):
    async def run(self, value=1):
        print('Value:', value)

        return value