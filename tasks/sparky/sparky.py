from pipeline.flows import SparkFlow


class SparkyTask(SparkFlow):
    # perhaps packages should be defined per-task?
    packages = [
        'org.apache.hadoop:hadoop-aws:2.6.0',
        'com.amazonaws:aws-java-sdk-pom:1.10.34',
    ]

    async def run(self, spark, **inputs):
        print('dataframe test')

        df = spark.read.csv(
            's3a://stackpoint-spark/random/test_csv/20141212.csv.gz',
            header=True,
            inferSchema=True,
        )

        df.limit(5).show()

        count = df.count()
        print(count, 'dataframe records')

        return {
            'record': count,
        }
