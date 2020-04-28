from cowait.tasks import Task, join
from lazy import Lazy


class Parent(Task):
    async def run(self, duration, count: int = 2, **inputs):
        # spawn a bunch of tasks using a list comprehension:
        tasks = [
            self.spawn(Lazy, duration=duration)
            for _ in range(0, count)
        ]

        # join() waits for a list of tasks to finish
        # it returns their results as a list:
        print('waiting for children to finish...')
        results = await join(tasks)

        print('all done')
        return results
