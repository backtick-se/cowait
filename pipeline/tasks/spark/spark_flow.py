import os  # stinky, dont read envs here
import asyncio
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pipeline.tasks import Task, Flow, sleep
from pipeline.network import get_local_ip

MSG_LEADER = 'I have been elected leader!'
MSG_REGISTER = 'Successfully registered with master'

SPARK_PACKAGES = [
    'com.amazonaws:aws-java-sdk-pom:1.11.375',
    'org.apache.hadoop:hadoop-aws:3.2.0',
]

SPARK_DEFAULTS = {
    'spark.executor.instances': '2',
    'spark.dynamicAllocation.enabled': 'true',

    # packages
    'spark.jars.packages': ','.join(SPARK_PACKAGES),

    # hadoop config
    'spark.hadoop.fs.s3a.access.key': os.getenv('AWS_ACCESS_KEY_ID'),
    'spark.hadoop.fs.s3a.secret.key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'spark.hadoop.fs.s3a.endpoint': 's3-eu-west-1.amazonaws.com',

    # 'spark.hadoop.fs.s3a.committer.magic.enabled': 'true',
    # 'spark.hadoop.fs.s3a.committer.name': 'magic',

    'spark.hadoop.fs.s3a.path.style.access': 'true',
    'spark.hadoop.fs.s3a.fast.upload': 'true',
    'spark.hadoop.fs.s3a.fast.upload.buffer': 'bytebuffer',
    'spark.hadoop.fs.s3a.path.style.access': 'true',
    'spark.hadoop.fs.s3a.multipart.size': '128M',
    'spark.hadoop.fs.s3a.fast.upload.active.blocks': '4',
    'spark.hadoop.fs.s3a.committer.name': 'partitioned',
}


def conf_from_cluster(app_name, master, config):
    sc = SparkConf() \
        .setAppName(app_name) \
        .setMaster(master)
    for option, value in config.items():
        sc.set(option, value)
    return sc


class SparkFlow(Flow):
    def __init__(self, taskdef, cluster, node):
        super().__init__(taskdef, cluster, node)
        self.master = None
        self.workers = []
        self.spark_cluster = {}

    async def on_log(self, id, file, data, **msg) -> None:
        if self.master and id == self.master.id:
            if MSG_LEADER in data:
                print('~~ spark master ready')
                self.master.ready.set_result(self.master)

        for worker in self.workers:
            if id == worker.id and MSG_REGISTER in data:
                print(f'~~ spark worker {worker.id} ready')
                worker.ready.set_result(worker)

    async def before(self, inputs: dict) -> dict:
        inputs = await super().before(inputs)

        # subscribe to logs
        self.node.children.on('log', self.on_log)

        # create cluster
        await self.setup_cluster()

        # create spark context
        # perhaps this should be optional?
        # in case no spark code is run in the flow itself
        if True:
            conf = conf_from_cluster(**self.spark_cluster)
            conf.set('spark.driver.host', get_local_ip())

            print('~~ starting spark session')
            self.spark = SparkSession.builder \
                .config(conf=conf) \
                .getOrCreate()

            print('~~ spark session ready')
            inputs['spark'] = self.spark

        return inputs

    async def after(self, inputs: dict):
        print('~~ destroying spark cluster')
        self.master.destroy()
        for worker in self.workers:
            worker.destroy()

        await super().after(inputs)

    async def task(
        self,
        name: str,
        image: str = None,
        env: dict = {},
        **inputs,
    ) -> Task:
        return await super().task(
            name=name,
            image=image,
            env=env,
            **inputs,
            spark=self.spark_cluster,
        )

    async def setup_cluster(self, num_workers=2, **config) -> None:
        print(f'~~ creating spark cluster...')
        print(f'~~   num_workers = {num_workers}')

        # create spark master
        self.master = await self.task(
            name='pipeline.tasks.spark.SparkMaster',
            ports={
                '8080/tcp': '8080',
            },
        )
        self.master.ready = asyncio.Future()
        master_uri = f'spark://{self.master.ip}:7077'

        await sleep(1)

        # create spark workers
        self.workers = []
        for i in range(0, num_workers):
            w = await self.task(
                name='pipeline.tasks.spark.SparkWorker',
                env={
                    'SPARK_WORKER_CORES': '2',
                },
                master=master_uri,
            )
            w.ready = asyncio.Future()
            self.workers.append(w)

        print('~~ waiting for cluster nodes')
        tasks = [
            self.master.ready,
            *map(lambda w: w.ready, self.workers),
        ]
        await asyncio.gather(*tasks)

        self.spark_cluster = {
            'app_name': self.id,
            'master': master_uri,
            'config': {
                **SPARK_DEFAULTS,
                **config,
            },
        }
