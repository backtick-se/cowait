import time
import random
from pipeline.tasks import Flow, join
from lazy.lazy import Lazy


class LazyParentTask(Flow):
    image = 'docker.backtick.se/parent'

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

        async def make_task():
            return await self.task(
                name='lazy',
                image=Lazy.image,
                block=block,
                duration=random.randint(duration, max_duration),
                crash_at=crash_at)

        if concurrent:
            tasks = [await make_task() for _ in range(0, count)]
            print('waiting for tasks')
            
            print('block for a bit')
            time.sleep(10)

            return await join(*tasks)

        else:
            async def await_task():
                task = await make_task()
                return await task.result

            return [await await_task() for _ in range(0, count)]
