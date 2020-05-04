from cowait import Task, join
from sleep import Sleep


class Parent(Task):
    async def run(self, duration, count: int = 2, **inputs):
        # spawn a bunch of tasks using a list comprehension:
        tasks = [
            Sleep(duration=duration) for _ in range(0, count)
        ]

        # join() waits for a list of tasks to finish
        # it returns their results as a list:
        print('waiting for children to finish...')
        results = await join(tasks)

        print('all done')
        return results
