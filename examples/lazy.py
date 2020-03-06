"""
Example task: Does nothing for X seconds.

Inputs:
    duration (int): Number of seconds to sleep

Outputs:
    duration (int): Number of seconds slept
"""
import time
import asyncio
from pipeline.tasks import Task
from duration_decider import DurationDecider


class Lazy(Task):
    async def run(self, duration: int = 0, block=False, crash_at=-1, **inputs):
        if duration == 0:
            duration = await self.spawn(DurationDecider)

        print('sleeping...')
        if block:
            print('running in blocking mode')

        for i in range(1, int(duration)+1):
            if crash_at and i == crash_at:
                raise RuntimeError(f'planned crash at {i}')

            print('slept', i)
            if block:
                time.sleep(1)
            else:
                await asyncio.sleep(1)

        print('rest level ok')

        return {
            'duration': duration,
            'crash_at': crash_at,
        }
