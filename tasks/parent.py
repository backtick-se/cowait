import random
from pipeline.tasks import Task, join
from lazy import Lazy


class LazyParentTask(Task):
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
            return self.spawn(
                Lazy,
                block=block,
                duration=random.randint(duration, max_duration),
                crash_at=crash_at)

        if concurrent:
            print('concurrent mode')
            tasks = [make_task() for _ in range(0, count)]
            return await join(*tasks)
        else:
            print('sequential mode')
            return [await make_task() for _ in range(0, count)]
