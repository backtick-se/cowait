from pipeline.tasks import Task


class TensorflowTask(Task):
    async def run(self, **inputs):
        print('hello tensorflow')


