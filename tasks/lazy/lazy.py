"""
Example task: Does nothing for X seconds.

Inputs:
    duration (int): Number of seconds to sleep

Outputs:
    duration (int): Number of seconds slept
"""
import asyncio
from pipeline.tasks import Task


class Lazy(Task):
    async def run(self, duration, crash_at=-1, **inputs):
        print('sleeping...')

        for i in range(1, int(duration)+1):
            if crash_at and i == crash_at:
                raise RuntimeError(f'planned crash at {i}')

            print('slept', i)
            await asyncio.sleep(1)

        print('rest level ok')

        return {
            'duration': duration,
            'crash_at': crash_at,
        }
