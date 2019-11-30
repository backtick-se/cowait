from pipeline.flows import SparkFlow


class SparkyTask(SparkFlow):
    async def run(self, spark, **inputs):
        print('dataframe test')

        df = spark.createDataFrame([
            {'name': 'johan', 'items': 3},
            {'name': 'erik', 'items': 1},
            {'name': 'andreas', 'items': 44},
        ])

        df.show()

        count = df.count()
        print(count, 'dataframe records')

        return count
