from pyspark.sql import SparkSession
from pipeline.tasks import Task
from pipeline.network import get_local_ip
from .spark_flow import conf_from_context


class SparkTask(Task):
    async def before(self, inputs: dict) -> dict:
        if 'spark' not in inputs:
            raise RuntimeError('Spark context not found in input')

        conf = conf_from_context(**inputs['spark'])
        conf.set('spark.driver.host', get_local_ip())

        print('~~ starting spark session')
        inputs['spark'] = SparkSession.builder \
            .config(conf=conf) \
            .getOrCreate()

        return inputs
