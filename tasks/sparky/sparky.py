import asyncio
from pyspark.sql import SparkSession
from pipeline.flows import Flow
from pipeline.tasks import sleep

from pyspark.conf import SparkConf


class SparkTask(Flow):
    logs = True
    master = None
    workers = []

    def handle(self, id: str, type: str, **msg):
        if type == 'log':
            if self.master:
                if id == self.master.id:
                    if 'I have been elected leader!' in msg['data']:
                        print('~~ spark master ready')
                        self.master.ready.set_result(self.master)

            for worker in self.workers:
                if id == worker.id:
                    if 'Successfully registered with master' in msg['data']:
                        print(f'~~ spark worker {worker.id} ready')
                        worker.ready.set_result(worker)

        if self.logs:
            super().handle(id, type, **msg)

    async def plan(self, num_workers: int = 2, **inputs):
        # create spark master
        self.master = await self.task(
            name='shell',
            image=self.image,
            command=' '.join([
                'spark-class',
                'org.apache.spark.deploy.master.Master',
            ]),
            env={
                'SPARK_WORKER_CORES': '1',
                'SPARK_WORKER_MEMORY': '1g',
            },
        )
        self.master.ready = asyncio.Future()
        master_uri = f'spark://{self.master.id}:7077'

        # give master a little head start
        await sleep(3)

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
                    'SPARK_WORKER_CORES': '1',
                    'SPARK_WORKER_MEMORY': '1g',
                },
            )
            w.ready = asyncio.Future()
            self.workers.append(w)

        print('waiting for cluster')
        tasks = [
            self.master.ready,
            *map(lambda w: w.ready, self.workers),
        ]
        await asyncio.gather(*tasks)

        print('cluster ready')

        conf = SparkConf() \
            .setAppName(self.id) \
            .setMaster(master_uri) \
            .set('spark.cores.max', '3') \
            .set('spark.executor.cores', '1') \
            .set('spark.executor.memory', '800m') \
            .set('spark.driver.cores', '1') \
            .set('spark.driver.memory', '800m')

        try:
            print('starting session')
            spark = SparkSession.builder \
                .config(conf=conf) \
                .getOrCreate()

            # spark.sparkContext.setLogLevel('FATAL')

            print('dataframe test')
            df = spark.createDataFrame([
                {'name': 'johan', 'items': 3},
                {'name': 'erik', 'items': 1},
                {'name': 'andreas', 'items': 44},
            ])

            df.show()

            # df.createGlobalTempView("items")

        finally:
            print('destroying cluster')
            self.master.destroy()
            for worker in self.workers:
                worker.destroy()

        return {}
