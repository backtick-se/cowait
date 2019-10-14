import random
import asyncio
from pipeline.flows import Flow


class LazyParentTask(Flow):
    async def plan(self, duration, max_duration = 0, count = 2, crash_at = -1, **inputs):

        if max_duration < duration:
            max_duration = duration

        tasks = [ ]
        for _ in range(0, count):
            t = self.task(
                name='lazy',
                image='johanhenriksson/pipeline-task:lazy', 
                duration=random.randint(duration, max_duration),
                crash_at=crash_at,
            )
            tasks.append(t)

        return await asyncio.gather(*tasks)
