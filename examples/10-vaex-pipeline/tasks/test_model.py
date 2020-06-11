from cowait import Task
from sklearn.metrics import accuracy_score
import vaex


class TestModel(Task):
    async def run(self, inpath, state):
        df = vaex.open(inpath)
        df.state_set(state)

        acc = accuracy_score(y_true=df['DOLocationID'].values,
                             y_pred=df.prediction.values)

        print(f"Accuracy {acc*100.}%")