import time
import random
from pipeline.tasks import Flow, join
from lazy import Lazy


class LazyParentTask(Flow):
    async def run(
        self,
        duration,
        max_duration=0,
        count=2,
        crash_at=-1,
        concurrent=True,
        block=False,
        **inputs,
    ):
        if max_duration < duration:
            max_duration = duration

        def make_task():
            return self.task(
                Lazy,
                block=block,
                duration=random.randint(duration, max_duration),
                crash_at=crash_at)

        if concurrent:
            tasks = [make_task() for _ in range(0, count)]
            print('waiting for tasks')
            print(tasks)

            print('block for a bit')
            time.sleep(3)
            print('done blocking')

            return await join(*tasks)

        else:
            print('sequential mode')
            results = []
            for _ in range(0, count):
                results.append(await make_task())
            return results
