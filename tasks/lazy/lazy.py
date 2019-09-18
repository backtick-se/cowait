"""
Example task: Does nothing for X seconds.

Inputs:
    duration (int): Number of seconds to sleep

Outputs:
    duration (int): Number of seconds slept
"""
import time

class Lazy(object):
    def run(self, context, inputs):
        print('sleeping...')
        duration = inputs['duration']

        for i in range(0, int(duration)):
            print('count:', i+1)
            time.sleep(1)

        print('done being lazy')

        return {
            'duration': duration
        }