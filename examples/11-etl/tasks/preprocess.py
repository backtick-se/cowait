import numpy as np
import pandas as pd
import fastparquet

from cowait import Task
from util import get_fs


class Preprocess(Task):
    async def run(self, inpath, storage):
        fs       = storage.aws
        df       = pd.read_csv(fs.open(inpath))
        orig_len = len(df)

        # Fix types, save some memory
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
        trip_seconds = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds()
        df           = df[(trip_seconds > 60) & (trip_seconds < 10800)]

        # remove outliers related to fare price
        df  = df[(df['fare_amount'] > 0) & (df['fare_amount'] < 3000)]

        print('Removed', orig_len - len(df), 'outlier rows')
        print('Total number of new rows:', len(df))

        # Save the result to S3
        outpath = 's3://backtick-internal/simple-pipeline/preprocess.parquet'
        
        # df.to_parquet(
        #     's3://backtick-internal/simple-pipeline/preprocess1.parquet',
        #     compression='gzip',
        #     open_with=fs
        # )

        fastparquet.write(
            outpath, df, compression='GZIP', open_with=fs
        )
        
        # with fs.open(outpath, 'w') as f:
        #     df.to_csv(f)

        return outpath