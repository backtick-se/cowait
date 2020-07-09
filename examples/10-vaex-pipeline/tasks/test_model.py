import vaex, json

from cowait import Task
from cowait.types import FileType
from sklearn.metrics import accuracy_score
from utils import vaex_open

class TestModel(Task):
    async def run(self, file: FileType, state_file: FileType) -> float:
        df    = vaex_open(file)
        state = json.load(state_file)
        
        df.state_set(state)

        acc = accuracy_score(y_true=df['DOLocationID'].values,
                             y_pred=df.prediction.values)

        return acc