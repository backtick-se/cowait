from pipeline.tasks import Task, join
from number import Number

class Minimum(Task):
    async def run(self, value1=1, value2=2, value3=3):
        tasks = [
            self.spawn(Number, value=value1),
            self.spawn(Number, value=value2),
            self.spawn(Number, value=value3)
        ]

        result = min(await join(*tasks))
        print('Minimum value:', result)

        return result