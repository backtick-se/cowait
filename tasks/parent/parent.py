import random
from pipeline.flows import Flow, join
from lazy.lazy import Lazy


class LazyParentTask(Flow):
    async def plan(
        self,
        duration,
        max_duration=0,
        count=2,
        crash_at=-1,
        concurrent=True,
        **inputs,
    ):
        if max_duration < duration:
            max_duration = duration

        def make_task():
            return self.task(
                name='lazy',
                image=Lazy.image,
                duration=random.randint(duration, max_duration),
                crash_at=crash_at)

        if concurrent:
            tasks = [make_task() for _ in range(0, count)]
            return await join(*tasks)
        else:
            return [await make_task() for _ in range(0, count)]
