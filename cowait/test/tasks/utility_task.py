import os
import json
from cowait.tasks import Task, sleep


class UtilityTask(Task):
    """
    Test utility container
    """

    def __init__(self, taskdef, cluster, node):
        super().__init__(taskdef, cluster, node)
        # store taskdef for later comparison
        self.taskdef = taskdef

    async def run(self, **inputs):
        # dump task information to stdout
        print(json.dumps({
            'taskdef': self.taskdef.serialize(),
            'env': dict(os.environ),
        }))

        # create a child
        if inputs.get('child', False):
            await self.spawn('cowait.test.tasks.utility_task')

        # run forever
        if inputs.get('forever', False):
            while True:
                await sleep(1)

        # return desired output
        return inputs.get('return', {})
