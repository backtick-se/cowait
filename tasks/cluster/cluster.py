from pipeline.tasks import sleep
from pipeline.tasks.spark import SparkFlow


class SparkClusterTask(SparkFlow):
    async def run(self, **inputs):
        while True:
            await sleep(1)
