import s3fs
import pandas as pd
import vaex

## Ideally supports all fsspec implementations, had a hard time implementing this for vaex.open, so hardcoded to s3
## https://github.com/vaexio/vaex/issues/733
def vaex_open(f):
    f = vaex.file.s3.open(f's3://{f.path}', key='minio', secret='minio123', client_kwargs=f.fs.client_kwargs)

    return vaex.hdf5.dataset.Hdf5MemoryMapped(f)

## export to s3? Local workaround which makes the files show up in minio browser
def vaex_export(df, f):
    df.export(f'data/{f.path}')


def get_classes():
    fs    = s3fs.S3FileSystem(anon=True)
    zones = pd.read_csv(fs.open('s3://cowait/zones.csv'))

    return [int(x) for x in zones['LocationID'].unique()]