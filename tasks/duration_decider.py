from pipeline.tasks import Task


class DurationDecider(Task):
    async def run(self):
        return 8
