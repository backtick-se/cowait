from pipeline.tasks import Task

import dask
import dask.dataframe as dd
import s3fs


class DaskExample(Task):
    async def run(self):
        # read in all files with bitmex trades during 2015
        ddf = dd.read_csv(f's3://stackpoint-spark/data/bitmex/trades/2015*.csv.gz', compression='gzip', blocksize=None)

        # add the traded amount as a column
        ddf['amount'] = ddf['size'] * ddf['price']

        # group on 'side', i.e. buy/sell
        ddf_side = ddf.groupby('side')

        # number of buys/sells 
        ddf_trades = ddf_side.size()

        # total bought/sold volume
        ddf_volume = ddf_side['size'].sum()

        # total bought/sold amount
        ddf_amount = ddf_side['amount'].sum()

        # compute the task graphs
        ddf_trades_res, ddf_volume_res, ddf_amount_res = dask.compute(ddf_trades, ddf_volume, ddf_amount)

        # get the different values
        trades_buy = ddf_trades_res['Buy']
        trades_sell = ddf_trades_res['Sell']
        trades = trades_buy + trades_sell
        volume_buy = ddf_volume_res['Buy']
        volume_sell = ddf_volume_res['Sell']
        volume = volume_buy + volume_sell
        amount_buy = ddf_amount_res['Buy']
        amount_sell = ddf_amount_res['Sell']
        amount = amount_buy + amount_sell

        result = {
            'Number of buys': int(trades_buy),
            'Number of sells': int(trades_sell),
            'Number of trades': int(trades),
            'Total volume bought': int(volume_buy),
            'Total volume sold': int(volume_sell),
            'Total volume traded': int(volume),
            'Total amount bought': int(amount_buy),
            'Total amount sold': int(amount_sell),
            'Total amount traded': int(amount)
        } 

        return result
        
