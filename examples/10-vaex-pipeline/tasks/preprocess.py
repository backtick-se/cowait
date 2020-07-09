import vaex
import numpy as np

from cowait import Task
from cowait.types import FileType
from utils import vaex_open, vaex_export

class Preprocess(Task):
    async def run(self, file: FileType, size: str) -> FileType:
        print(file)
        df       = vaex_open(file)
        orig_len = len(df)

        # Fix types, saves some memory (& disk space when dumping to hdf5)
        df['VendorID']              = df['VendorID'].astype('uint8')
        df['payment_type']          = df['payment_type'].astype('uint8')
        df['RatecodeID']            = df['RatecodeID'].astype('uint8')
        df['passenger_count']       = df['passenger_count'].astype('uint8')
        df['store_and_fwd_flag']    = df['store_and_fwd_flag'].apply(lambda x: 1 if x == 'Y' else 0).astype('bool')
        df['payment_type']          = df['payment_type'].astype('uint8')
        df['PULocationID']          = df['PULocationID'].astype('uint16')
        df['DOLocationID']          = df['DOLocationID'].astype('uint16')
        df['tpep_pickup_datetime']  = df['tpep_pickup_datetime'].astype('datetime64')
        df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].astype('datetime64')

        # Remove data that's not from 2019
        df = df[df['tpep_pickup_datetime'].dt.year == 2019]

        # keep trips between 1 minute and 3 hours
        trip_seconds = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).td.total_seconds()
        df           = df[(trip_seconds > 60) & (trip_seconds < 10800)]

        # remove outliers related to fare price
        df  = df[(df['fare_amount'] > 0) & (df['fare_amount'] < 3000)]

        print('Removed', orig_len - len(df), 'outlier rows')
        print('Total number of new rows:', len(df))

        with self.storage.minio.open(f'taxi/{size}/processed.hdf5') as f:
            vaex_export(df, f)

        return f