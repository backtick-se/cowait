from cowait import Task, join
from number import Number


class Minimum(Task):
    async def run(self, first=3, second=5):
        tasks = [
            Number(value=first),
            Number(value=second)
        ]

        result = min(await join(tasks))

        print('Minimum value:', result)

        return result
