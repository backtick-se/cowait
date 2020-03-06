from pipeline.tasks import Task


class EchoTask(Task):
    async def run(self, **inputs):
        return inputs
