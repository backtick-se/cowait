import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from pipeline.flows import SparkFlow

TIMESTAMP = "yyyy-MM-dd'D'HH:mm:ss.SSS"

BitmexTrades = StructType([
    StructField('timestamp', StringType(), True),
    StructField('symbol', StringType(), True),
    StructField('side', StringType(), True),
    StructField('size', IntegerType(), True),
    StructField('price', FloatType(), True),
    StructField('tickDirection', StringType(), True),
    StructField('trdMatchID', StringType(), True),
    StructField('grossValue', IntegerType(), True),
    StructField('homeNotional', FloatType(), True),
    StructField('foreignNotional', FloatType(), True),
])


class SparkyTask(SparkFlow):
    async def run(
        self,
        spark,
        filter='2014*',
        start='2014-01-01',
        end='2015-01-01',
        mode='append',
        **inputs,
    ):
        print('bitmex trades csv->parquet')

        df = spark.read \
            .csv(
                f's3a://stackpoint-spark/data/bitmex/trades/{filter}.csv.gz',
                header=True,
                schema=BitmexTrades,
            )

        # df.timestamp.cast(DateType())

        df = df.filter(df.timestamp >= start) \
               .filter(df.timestamp < end)

        df = df.drop('grossValue')
        df = df.drop('homeNotional')
        df = df.drop('foreignNotional')

        # cut milli/nanoseconds and convert to timestamp
        df = df.withColumn("timestamp", F.to_timestamp(F.substring(df.timestamp, 0, 23), TIMESTAMP))

        # create partitioning columns
        df = df.withColumn("year", F.year(df.timestamp))
        df = df.withColumn("month", F.month(df.timestamp))
        df = df.withColumn("day", F.dayofmonth(df.timestamp))

        df.limit(5).show()

        count = df.count()
        print(f'{count} trades')

        volume = df.agg(F.sum("size")).collect()[0][0]
        print(f'total volume: ${volume}')

        print('writing parquet')
        df.write \
            .mode(mode) \
            .partitionBy(['year', 'month', 'day']) \
            .parquet('s3a://stackpoint-spark/data/bitmex/parquet/trades')

        print('done writing')
        return {
            'trades': count,
            'volume': volume,
        }
