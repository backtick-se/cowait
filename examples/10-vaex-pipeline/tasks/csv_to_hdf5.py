import vaex, s3fs
from cowait import Task
from utils import get_outpath


class CsvToHdf5(Task):
    async def run(self, inpath, size):
        print("Reading data to dataframe, input path:", inpath)
        fs = s3fs.S3FileSystem(anon=True)

        outpath = get_outpath(size, 'taxi.hdf5')
        
        with fs.open(inpath, "r") as f:
            vaex.from_csv(f, convert=outpath)

        return outpath