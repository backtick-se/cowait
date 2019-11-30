from .task import Task
from pyspark.sql import SparkSession
from .spark_flow import conf_from_context


class SparkTask(Task):
    async def before(self, inputs: dict) -> dict:
        if 'spark' not in inputs:
            raise RuntimeError('Spark context not found in input')

        # prepare spark context
        conf = conf_from_context(**inputs['spark'])

        print('~~ starting spark session')
        inputs['spark'] = SparkSession.builder \
            .config(conf=conf) \
            .getOrCreate()

        return inputs
