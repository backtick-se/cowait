import vaex, s3fs

from cowait import Task
from cowait.types import FileType
from utils import vaex_open, vaex_export


class CsvToHdf5(Task):
    async def run(self, inpath: str, size: str) -> FileType:
        print("Reading CSV data to dataframe, input path:", inpath)

        df = vaex.open(f'{inpath}?anon=True')
        
        print(self.storage.minio)

        f = self.storage.minio.open(f'taxi/{size}/taxi.hdf5', 'wb')

        vaex_export(df, f)

        return f    # returns a <S3File> handle to the written file.
