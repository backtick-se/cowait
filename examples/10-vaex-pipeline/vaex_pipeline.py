from cowait import Task
from tasks import CsvToHdf5, Preprocess, TrainTestSplit, TrainModel, TestModel


class VaexPipeline(Task):
    async def run(self, size='xsmall'):
        assert size in ['xsmall', 'small', 'medium', 'large']

        s3_path     = f's3://cowait/yellow_2019-{size}.csv'

        hdf5        = await CsvToHdf5(inpath=s3_path, size=size)
        processed   = await Preprocess(file=hdf5, size=size)
        train, test = await TrainTestSplit(file=processed, test_size=0.25, size=size)

        model       = await TrainModel(file=train, size=size)
        test_acc    = await TestModel(file=test, state_file=model['state'])

        return {
            'alpha': model['alpha'],
            'train_acc': model['acc'],
            'test_acc': test_acc,
        }
