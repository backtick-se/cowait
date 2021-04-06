from cowait.tasks import Task
from cowait.tasks.notebook import NotebookRunner
import numpy as np

class GetData(Task):
    async def run(self, N: int = 5):
        sequence = None
        
        work = await NotebookRunner(path='extra_work.ipynb', N=N)

        if work['success']:
            sequence = work['result']
        else:
            print(f"Worker failed. Error: {work['error']}")
        
        return {
            'sequence': sequence
        }
