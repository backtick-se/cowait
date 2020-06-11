from cowait import Task
import vaex


class SanityCheck(Task):
    async def run(self, inpath, state):
        fs    = s3fs.S3FileSystem(anon=True)
        zones = pd.read_csv(fs.open('s3://cowait/zones.csv')

        # starting points
        df = pd.DataFrame([
            [43,   7, 0],      # Manhattan, central park,  07.00, monday
            [132, 15, 3]       # JFK, 15.00, thursday
            [43,  23, 4],      # Manhattan, central park,  23.00, friday
            [29,   9, 5]       # Brooklyn, Brighton beach, 09.00, saturday
            [261,  9, 6]       # Manhattan, World Trade Center, 09.00, saturday
        ], columns=['PULocationID', 'dayofweek', 'hour'])
        
        df = vaex.from_pandas(df)
        df.state_set(state)

        # TODO map zones to nrs, output nicely
        print(df)