"""
Example task: Does nothing for X seconds.

Inputs:
    duration (int): Number of seconds to sleep

Outputs:
    duration (int): Number of seconds slept
"""
import asyncio
from cowait import Task


class Sleep(Task):
    async def run(self, duration: int = 2, **inputs):
        print('sleeping...')

        # wait for a while
        for i in range(0, int(duration)):
            print('slept', i+1)
            await asyncio.sleep(1)

        # return the duration slept
        return {
            'duration': duration,
        }
