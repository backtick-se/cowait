from pyspark.sql import Row
from pipeline.flows import SparkFlow


class SparkyTask(SparkFlow):
    async def run(self, spark, **inputs):
        print('dataframe test')

        df = spark.createDataFrame([
            Row(name='johan', items=3),
            Row(name='erik', items=1),
            Row(name='andreas', items=44),
        ])

        df.show()

        count = df.count()
        print(count, 'dataframe records')

        return count
