from pipeline.tasks import sleep
from pipeline.flows import SparkFlow


class SparkClusterTask(SparkFlow):
    async def run(self, **inputs):
        while True:
            await sleep(1)
