from cowait import Task, join
from .fit import Fit
import vaex


class TrainModel(Task):
    async def run(self, inpath):
        df = vaex.open(inpath)

        classes = [int(x) for x in df['DOLocationID'].unique()]
        alphas  = [0.1, 0.5, 1.0]

        # parallel parameter search
        tasks   = [Fit(inpath=inpath, alpha=a, classes=classes) for a in alphas]
        results = await join(tasks)

        winner  = max(results, key=lambda x: x['acc'])

        print('Best fit: alpha=', winner['alpha'])
        
        return winner['state']