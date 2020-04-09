from pipeline.tasks import Task

class Maximum(Task):
    async def run(self, value1=1, value2=2, value3=3):
        a = await Number(value=value1)
        b = await Number(value=value2)
        c = await Number(value=value3)

        return max(a, b, c)