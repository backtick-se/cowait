from pyspark.sql import SparkSession
from cowait.tasks import Task
from cowait.network import get_local_ip
from .spark_cluster import conf_from_cluster


class SparkTask(Task):
    async def before(self, inputs: dict) -> dict:
        if 'spark' not in inputs:
            raise RuntimeError('Spark context not found in input')

        conf = conf_from_cluster(**inputs['spark'])
        conf.set('spark.driver.host', get_local_ip())

        print('~~ starting spark session')
        inputs['spark'] = SparkSession.builder \
            .config(conf=conf) \
            .getOrCreate()

        return inputs
