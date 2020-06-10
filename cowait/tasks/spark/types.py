from pyspark.conf import SparkConf
from cowait.network import get_local_ip
from cowait.types import Type, TypeAlias


@TypeAlias(SparkConf)
class SparkConfType(Type):
    name: str = 'SparkConf'

    def validate(self, conf: SparkConf, name: str) -> None:
        if not isinstance(conf, dict):
            raise ValueError(f'{name} is not a SparkConf')

    def serialize(self, conf: SparkConf):
        # serialize spark configuration
        return {key: value for key, value in conf.getAll()}

    def deserialize(self, config: dict):
        conf = SparkConf()
        for option, value in config.items():
            conf.set(option, value)

        # set driver host to our local ip
        conf.set('spark.driver.host', get_local_ip())

        return conf
