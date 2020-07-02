from cowait import Task
from tasks import Preprocess# TrainTestSplit, TrainModel, TestModel


class EtlPipeline(Task):
    async def run(self, size='xsmall'):
        assert size in ['xsmall', 'small', 'medium', 'large']

        s3_path     = f's3://cowait/yellow_2019-{size}.csv'
        storage     = self.storage

        # processed   = await Preprocess(inpath=s3_path, storage=storage)

        # processed   = await Preprocess(inpath=s3_path, size=size)
        # train, test = await TrainTestSplit(inpath=processed, test_size=0.25, size=size)

        # model       = await TrainModel(inpath=train, size=size)
        # test_acc    = await TestModel(inpath=test, state_path=model['path'])

        # return {
        #     'alpha': model['alpha'],
        #     'train_acc': model['acc'],
        #     'test_acc': test_acc,
        # }

        ##### Preprocess #####
        import pandas as pd
        import fastparquet


        inpath   = s3_path
        fs       = self.storage.aws
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
        
        fastparquet.write(
            outpath,
            df,
            compression='gzip',
            open_with=fs.open
        )


        ##### Train/Test split #####
        from sklearn.model_selection import train_test_split


        inpath    = outpath
        test_size = 0.25
        fs        = self.storage.aws
        df        = pd.read_parquet(fs.open(inpath, compression='gzip'))
 
        # Create some features
        df['dayofweek']  = df['tpep_pickup_datetime'].dt.dayofweek
        df['hour']       = df['tpep_pickup_datetime'].dt.hour
        df = df[['PULocationID', 'hour', 'dayofweek', 'DOLocationID']]

        # Split
        df_train, df_test = train_test_split(df, test_size=test_size)

        # Store
        outpath_train = 's3://backtick-internal/simple-pipeline/train.parquet'
        outpath_test  = 's3://backtick-internal/simple-pipeline/test.parquet'

        fastparquet.write(
            outpath_train,
            df_train,
            compression='gzip',
            open_with=fs.open
        )

        fastparquet.write(
            outpath_test,
            df_test,
            compression='gzip',
            open_with=fs.open
        )


        ##### Fit #####
        from sklearn.naive_bayes import CategoricalNB
        from sklearn.metrics import accuracy_score
        import pickle


        inpath = outpath_train
        fs     = self.storage.aws
        df     = pd.read_parquet(fs.open(inpath, compression='gzip'))
        # alphas = [0.1, 0.5, 1.0]
        alpha  = 0.5 
        model  = CategoricalNB(alpha=alpha)
        X      = df[['PULocationID', 'dayofweek', 'hour']]
        y      = df['DOLocationID']
        clf    = model.fit(X, y)
        df['prediction'] = clf.predict(X)
        

        acc = accuracy_score(y_true=df['DOLocationID'].values,
                             y_pred=df['prediction'].values)


        print('acc', acc)
        print(df.head())

        ### Store the model
        outpath = 's3://backtick-internal/simple-pipeline/model.pkl'

        pickle.dump(clf, fs.open(outpath,'wb'))

        ##### Load the model #####
        loaded_clf = pickle.load(fs.open(outpath, 'rb'))
        preds      = loaded_clf.predict(X)
        
        print('loaded preds')
        print(preds)