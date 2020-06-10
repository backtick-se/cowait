from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from cowait.network import get_local_ip
from cowait.types import Type, TypeAlias


@TypeAlias(SparkSession)
class SparkSessionType(Type):
    name: str = 'SparkSession'

    def validate(self, session: SparkSession, name: str) -> None:
        if not isinstance(session, dict):
            raise ValueError(f'{name} is not a SparkSession')

        # todo: ensure required fields exist

    def serialize(self, session: SparkSession):
        # serialize spark configuration
        conf = session.sparkContext.getConf()
        return {
            key: value for key, value in conf.getAll()
        }

    def deserialize(self, session: dict):
        print('deserialize session', session)
        conf = SparkConf()
        for option, value in session.items():
            conf.set(option, value)

        # set driver host to our local ip
        conf.set('spark.driver.host', get_local_ip())

        return SparkSession.builder \
            .config(conf=conf) \
            .getOrCreate()
