from cowait import Task
import vaex, s3fs


class CsvToHdf5(Task):
    async def run(self, path):
        print("Reading data to dataframe")
        fs = s3fs.S3FileSystem(anon=True)

        with fs.open(path, 'r') as f:
            print("Writing data to hdf5")
            vaex.from_csv(f, convert='taxi_data.hdf5')

        return True
