import os  # stinky, dont read envs here
import asyncio
from concurrent.futures import Future
from pyspark.conf import SparkConf
from cowait.tasks import Task, sleep, rpc
from cowait.tasks.messages import TASK_LOG
from .master import SparkMaster
from .worker import SparkWorker


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


class SparkCluster(Task):
    def init(self):
        self.master = None
        self.workers = []
        self.spark_cluster = {}
        self.running = True
        self.app_name = self.id

        # subscribe to logs
        self.node.children.on(TASK_LOG, self.on_log)

    async def on_log(self, id, file, data, **msg) -> None:
        if self.master and id == self.master.id:
            if MSG_LEADER in data:
                print('~~ spark master ready')
                self.master.ready.set_result(self.master)

        for worker in self.workers:
            if id == worker.id and MSG_REGISTER in data:
                print(f'~~ spark worker {worker.id} ready')
                worker.ready.set_result(worker)

        return False

    async def before(self, inputs: dict) -> dict:
        # create cluster
        await self.setup_cluster(
            workers=inputs.get('workers'),
        )
        return inputs

    async def run(self, app_name: str = None, workers: int = 2):
        if app_name is not None:
            self.app_name = app_name

        if '/' in self.master.routes:
            print('Spark WebUI available at:')
            print(self.master.routes['/']['url'])

        while self.running:
            await sleep(1)

        return {}

    async def after(self, inputs: dict):
        print('~~ destroying spark cluster')
        self.master.destroy()
        for worker in self.workers:
            worker.destroy()

        await super().after(inputs)

    async def setup_cluster(self, workers=2, **config) -> None:
        print(f'~~ creating spark cluster...')
        print(f'~~   workers = {workers}')

        # create spark master
        self.master = SparkMaster(
            routes={'/': 8080},
        )
        self.master.ready = Future()
        self.master_uri = f'spark://{self.master.ip}:7077'

        await sleep(1)

        # create spark workers
        self.workers = []
        await self.add_workers(workers)

        print('~~ waiting for cluster nodes')
        await self.wait_for_nodes()

        print('~~ spark cluster ready')

    @rpc
    async def get_workers(self):
        ready = filter(lambda w: w.ready.done(), self.workers)
        ids = list(map(lambda w: w.id, ready))
        return {
            'workers': ids,
            'ready': len(ids),
            'total': len(self.workers),
        }

    @rpc
    async def scale(self, workers: int):
        diff = workers - len(self.workers)
        if diff > 0:
            # scale up
            print(f'~~ scale({workers}): adding {diff} workers')
            await self.add_workers(diff)

        elif diff < 0:
            # scale down
            print(f'~~ scale({workers}): removing {abs(diff)} workers')
            await self.remove_workers(diff)

    @rpc
    async def get_config(self) -> SparkConf:
        conf = SparkConf() \
            .setAppName(self.app_name) \
            .setMaster(self.master_uri)
        for option, value in SPARK_DEFAULTS.items():
            conf.set(option, value)
        return conf

    async def add_workers(self, count):
        for i in range(0, count):
            w = SparkWorker(
                master=self.master_uri,
                cores=2,
                routes={},
                ports={},
            )
            w.ready = Future()
            self.workers.append(w)

    async def remove_workers(self, count):
        count = abs(count)
        if count > len(self.workers):
            count = len(self.workers)

        for worker in self.workers[-count:]:
            worker.destroy()
        self.workers = self.workers[:-count]

    async def wait_for_nodes(self):
        await asyncio.gather(
            asyncio.wrap_future(self.master.ready),
            *map(lambda w: asyncio.wrap_future(w.ready), self.workers),
        )

    @rpc
    async def teardown(self) -> None:
        self.running = False
