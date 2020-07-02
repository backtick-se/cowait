# import os
# import pandas as pd

# from cowait import Task
# from utils import get_fs

# class TrainTestSplit(Task):
#     async def run(self, inpath, test_size, size):
#         fs = get_fs()
#         df = pd.read_csv(fs.open(inpath, mode='rb'))

#         # create some features
#         df['dayofweek']  = df['tpep_pickup_datetime'].dt.dayofweek
#         df['hour']       = df['tpep_pickup_datetime'].dt.hour

#         shuffle_path = get_outpath(size, 'shuffled.hdf5')
#         df.export(shuffle_path,
#                   column_names=['PULocationID', 'hour', 'dayofweek', 'DOLocationID'],
#                   shuffle=True)

#         df                = vaex.open(shuffle_path)
#         df_train, df_test = df.ml.train_test_split(test_size=test_size)

#         train_out = get_outpath(size, 'train.hdf5')
#         test_out  = get_outpath(size, 'test.hdf5')

#         df_train.export(train_out)
#         df_test.export(test_out)

#         os.remove(shuffle_path) # cleanup

#         return [train_out, test_out]