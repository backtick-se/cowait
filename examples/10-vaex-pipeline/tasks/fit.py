import vaex, json
from vaex.ml.sklearn import IncrementalPredictor
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_score

from cowait import Task
from utils import get_outpath, get_classes

class Fit(Task):
    async def run(self, inpath, alpha, size):
        model      = CategoricalNB(alpha=alpha)
        vaex_model = IncrementalPredictor(features=['PULocationID', 'dayofweek', 'hour'],
                                          target='DOLocationID',
                                          model=model, 
                                          batch_size=100_000, 
                                          partial_fit_kwargs={'classes': get_classes()}
                                         )

        df = vaex.open(inpath)
        vaex_model.fit(df=df, progress=True)

        df  = vaex_model.transform(df=df)
        acc = accuracy_score(y_true=df['DOLocationID'].values,
                             y_pred=df['prediction'].values)

        outpath = get_outpath(size, f'model-{self.id}.json') # task id used to seperate result output paths
        json.dump(df.state_get(), open(outpath, 'w'))

        return {
            'alpha': alpha,
            'acc': acc,
            'path': outpath
        }