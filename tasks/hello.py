from pipeline.tasks import Task


class Hello(Task):
    async def run(self, **inputs):
        print('hello world')
