from pipeline.tasks import Task
from number import Number

class Maximum(Task):
    async def run(self, value1=1, value2=2, value3=3):
        a = await self.spawn(Number, value=value1)
        b = await self.spawn(Number, value=value2)
        c = await self.spawn(Number, value=value3)

        result = max(a, b, c)
        print('Maximum value:', result)

        return result