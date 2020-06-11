from cowait import Task
from csv_to_hdf5 import CsvToHdf5
import vaex, s3fs

# one month of taxi data (yellow cab)
DATA_PATH = "s3://nyc-tlc/trip data/yellow_tripdata_2019-01.csv"


class VaexPipeline(Task):
    async def run(self, path=DATA_PATH):
        
        await CsvToHdf5(path=path)
        # await Preprocess()
        # await Train()

        return True
