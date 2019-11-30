import asyncio
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pipeline.flows import Flow
from pipeline.tasks import Task, sleep

MSG_LEADER = 'I have been elected leader!'
MSG_REGISTER = 'Successfully registered with master'


def conf_from_context(app_name, master, **spark):
    return SparkConf() \
        .setAppName(app_name) \
        .setMaster(master) \
        .set('spark.cores.max', spark.get('cores.max', 3)) \
        .set('spark.executor.cores', spark.get('executor.cores', 1)) \
        .set('spark.executor.memory', spark.get('executor.memory', '800m')) \
        .set('spark.driver.cores', spark.get('driver.cores', 1)) \
        .set('spark.driver.memory', spark.get('driver.memory', '800m'))


class SparkFlow(Flow):
    def __init__(self, taskdef, cluster, node):
        super().__init__(taskdef, cluster, node)
        self.master = None
        self.workers = []
        self.spark_config = {}
        self.spark_logs = taskdef.inputs.get('spark.logs', False)

    def handle(self, id: str, type: str, **msg) -> bool:
        if type == 'log':
            if not self.on_log(id=id, **msg):
                return False

        return super().handle(id, type, **msg)

    def on_log(self, id, file, data, **msg) -> bool:
        if self.master and id == self.master.id:
            if MSG_LEADER in data:
                print('~~ spark master ready')
                self.master.ready.set_result(self.master)

        for worker in self.workers:
            if id == worker.id and MSG_REGISTER in data:
                print(f'~~ spark worker {worker.id} ready')
                worker.ready.set_result(worker)

        return self.spark_logs

    async def before(self, inputs: dict) -> dict:
        inputs = await super().before(inputs)

        self.spark_config = await self.setup_cluster()

        print('~~ starting spark session')
        self.spark = SparkSession.builder \
            .config(conf=conf_from_context(**self.spark_config)) \
            .getOrCreate()

        inputs['spark'] = self.spark
        return inputs

    async def after(self, result, inputs):
        print('~~ destroying spark cluster')
        self.master.destroy()
        for worker in self.workers:
            worker.destroy()

        return await super().after(result, inputs)

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
            spark=self.spark_config,
        )

    async def setup_cluster(self, num_workers=2, **config) -> str:
        print(f'~~ creating spark cluster...')
        print(f'~~   num_workers = {num_workers}')

        # create spark master
        self.master = await self.task(
            name='shell',
            image=self.image,
            command=' '.join([
                'spark-class',
                'org.apache.spark.deploy.master.Master',
            ]),
            env={
                'SPARK_WORKER_CORES': config.get('worker.cores', 1),
                'SPARK_WORKER_MEMORY': config.get('worker.memory', '1g'),
            },
        )
        self.master.ready = asyncio.Future()
        master_uri = f'spark://{self.master.id}:7077'

        await sleep(1)

        # create spark workers
        self.workers = []
        for i in range(0, num_workers):
            w = await self.task(
                name='shell',
                image=self.image,
                command=' '.join([
                    'spark-class',
                    'org.apache.spark.deploy.worker.Worker',
                    master_uri,
                ]),
                env={
                    'SPARK_WORKER_CORES': config.get('worker.cores', 1),
                    'SPARK_WORKER_MEMORY': config.get('worker.memory', '1g'),
                },
            )
            w.ready = asyncio.Future()
            self.workers.append(w)

        print('~~ waiting for cluster nodes')
        tasks = [
            self.master.ready,
            *map(lambda w: w.ready, self.workers),
        ]
        await asyncio.gather(*tasks)

        return {
            'app_name': self.id,
            'master': master_uri,
            **config,
        }
