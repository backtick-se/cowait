import vaex, json

from cowait import Task
from sklearn.metrics import accuracy_score

class TestModel(Task):
    async def run(self, inpath, state_path):
        df    = vaex.open(inpath)
        state = json.load(open(state_path))
        
        df.state_set(state)

        acc = (df['DOLocationID'] == df['prediction']).sum() / len(df)

        return acc