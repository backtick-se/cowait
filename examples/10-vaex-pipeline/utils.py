import s3fs
import pandas as pd

def get_outpath(size, name):
    return f'output/{size}/{name}'

def get_classes():
    fs    = s3fs.S3FileSystem(anon=True)
    zones = pd.read_csv(fs.open('s3://cowait/zones.csv'))

    return [int(x) for x in zones['LocationID'].unique()]