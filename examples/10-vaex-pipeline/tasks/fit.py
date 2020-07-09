import vaex, json
from vaex.ml.sklearn import IncrementalPredictor
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_score

from cowait import Task
from cowait.types import FileType
from utils import vaex_open, vaex_export

class Fit(Task):
    async def run(self, file: FileType, alpha: float, size: str) -> dict:
        model      = CategoricalNB(alpha=alpha)
        vaex_model = IncrementalPredictor(features=['PULocationID', 'dayofweek', 'hour'],
                                          target='DOLocationID',
                                          model=model, 
                                          batch_size=100_000, 
                                          partial_fit_kwargs={'classes': get_classes()}
                                         )

        df = vaex_open(file)
        vaex_model.fit(df=df, progress=True)

        df  = vaex_model.transform(df=df)
        acc = accuracy_score(y_true=df['DOLocationID'].values,
                             y_pred=df['prediction'].values)

        # task id used to seperate result output paths
        with self.storage.minio.open(f'taxi/{size}/model_{self.id}.json') as f:
            json.dump(df.state_get(), f)

        return {
            'alpha': alpha,
            'acc': acc,
            'state': f
        }