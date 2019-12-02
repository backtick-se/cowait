import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, \
    TimestampType, IntegerType, FloatType
from pipeline.flows import SparkFlow


BitmexTrades = StructType([
    StructField('timestamp', TimestampType(), True),
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
    # perhaps packages should be defined per-task?
    packages = [
        'org.apache.hadoop:hadoop-aws:2.6.0',
        'com.amazonaws:aws-java-sdk-pom:1.10.34',
    ]

    async def run(
        self,
        spark,
        period='2014*',
        start='2014-01-01',
        end='2015-01-01',
        **inputs,
    ):
        print('bitmex trades csv->parquet')

        df = spark.read \
            .option('timestampFormat', "yyyy-MM-dd'D'HH:mm:ss.SSSSSS") \
            .csv(
                f's3a://stackpoint-spark/data/bitmex/trades/{period}.csv.gz',
                header=True,
                schema=BitmexTrades,
            )

        # df.timestamp.cast(DateType())

        df = df.filter(df.timestamp >= start) \
               .filter(df.timestamp < end)

        df = df.drop('grossValue')
        df = df.drop('homeNotional')
        df = df.drop('foreignNotional')

        df = df.withColumn("year", F.year(df.timestamp))
        df = df.withColumn("month", F.month(df.timestamp))
        df = df.withColumn("day", F.dayofmonth(df.timestamp))

        df = df.sort(df.timestamp.desc())

        df.limit(5).show()

        count = df.count()
        print(f'{count} trades')

        volume = df.agg(F.sum("size")).collect()[0][0]
        print(f'total volume: ${volume}')

        df.write \
            .mode("overwrite", "true") \
            .partitionBy(['year', 'month', 'day']) \
            .parquet('s3a://stackpoint-spark/data/bitmex/parquet/trades')

        return {
            'trades': count,
            'volume': volume,
        }
