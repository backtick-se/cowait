import s3fs, vaex, json
import pandas as pd

from cowait import Task, join
from utils import vaex_open, vaex_export
from .fit import Fit

class TrainModel(Task):
    async def run(self, file, size):
        df      = vaex_open(file)
        alphas  = [0.1, 0.5, 1.0]

        # parallel parameter search
        tasks   = [Fit(file=file, alpha=a, size=size) for a in alphas]
        results = await join(tasks)

        winner  = max(results, key=lambda x: x['acc'])

        print('Best fit: alpha=', winner['alpha'])
        
        return winner