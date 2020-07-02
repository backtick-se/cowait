import s3fs

def get_fs():
    return s3fs.S3FileSystem(
        anon    = False,
        key     = 'ASIAULLOEUCNMEZRQFHV',
        secret  = 'L6SGN+lihWJgdyFqHrrmBrEzJ8j8uzml1A6BvC6u',
        token   = 'FwoGZXIvYXdzEN///////////wEaDNWDXEILroQ+MZi6mCKGAS29FxsCDUNYIn++qmy8GDQOb/2AB/Agz0xY/PumXI6zbPBVt/8SW/0VLBRu+3WdahC8L1fSzevJctps0xHCfPasNwSh1U1xCerUKvvKbOXf9gUPVp1+pusLwPvzjWMvFrIIdVF8i88uWR6h+xeiIbaGZoVy8gcZ4PJ6TRvfYqFX1b9GZViOKLKZ+fcFMiiYOwEFzDduGJvSc2yEHHHYi4JFMVZif5QQC7CtINOscdRVdH7s6A+8'
    )