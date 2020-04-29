from cowait import Task
from number import Number


class Maximum(Task):
    async def run(self, first=3, second=5):
        a = await Number(value=first)
        b = await Number(value=second)

        result = max(a, b)

        print('Maximum value:', result)

        return result
