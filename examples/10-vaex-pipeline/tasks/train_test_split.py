import os, vaex

from cowait import Task
from cowait.types import FileType, List
from utils import vaex_open, vaex_export

FileList = List(FileType)

class TrainTestSplit(Task):
    async def run(self, file: FileType, test_size: float, size: str) -> FileList:
        df = vaex_open(file)

        # create some features
        df['dayofweek']  = df['tpep_pickup_datetime'].dt.dayofweek
        df['hour']       = df['tpep_pickup_datetime'].dt.hour

        with self.storage.minio.open(f'/taxi/{size}/shuffle.hdf5') as f:
            vaex_export(df, 
                        f,
                        column_names=['PULocationID', 'hour', 'dayofweek', 'DOLocationID'],
                        shuffle=True)

        df                = vaex_open(file_shuffle)
        df_train, df_test = df.ml.train_test_split(test_size=test_size)

        with self.storage.minio.open(f'taxi/{size}/train.hdf5') as train_out:
            vaex_export(df_train, train_out)

        with self.storage.minio.open(f'taxi/{size}/test.hdf5') as test_out:
            vaex_export(df_test, test_out)

        return [train_out, test_out]