from cowait import Task
import vaex
from vaex.ml.sklearn import IncrementalPredictor
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_score
import json

class Fit(Task):
    async def run(self, inpath, alpha, classes):
        model      = CategoricalNB(alpha=alpha)
        vaex_model = IncrementalPredictor(features=['PULocationID', 'dayofweek', 'hour'],
                                          target='DOLocationID',
                                          model=model, 
                                          batch_size=100_000, 
                                          partial_fit_kwargs={'classes': classes}
                                         )

        df = vaex.open(inpath)

        vaex_model.fit(df=df, progress=True)

        df  = vaex_model.transform(df=df)
        acc = accuracy_score(y_true=df['DOLocationID'].values,
                             y_pred=df['prediction'].values)

        return {
            'alpha': alpha,
            'acc': acc,
            'state': df.state_get()
        }