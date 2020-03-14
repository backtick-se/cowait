from pipeline.tasks import Task
from mnist_sample import do_tf_work

class TensorflowTask(Task):
    async def run(self, **inputs):
        do_tf_work()

