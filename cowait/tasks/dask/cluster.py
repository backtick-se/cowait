import asyncio
from cowait.tasks import Task, sleep, rpc
from cowait.tasks.messages import TASK_LOG
from concurrent.futures import Future
from dask.distributed import Client as DaskClient
from .worker import DaskWorker
from .scheduler import DaskScheduler
from .types import DaskClientType  # noqa: F401

MSG_LEADER = 'Scheduler at:'
MSG_REGISTER = 'Registered to:'


class DaskCluster(Task):
    def init(self):
        self.scheduler = None
        self.workers = []
        self.running = False

        # subscribe to logs
        self.node.server.on(TASK_LOG, self.on_log)

    async def on_log(self, id, file, data, **msg) -> None:
        if self.scheduler and id == self.scheduler.id:
            if MSG_LEADER in data:
                print('~~ dask scheduler ready')
                self.scheduler.ready.set_result(self.scheduler)

        for worker in self.workers:
            if id == worker.id and MSG_REGISTER in data:
                print(f'~~ dask worker {worker.id} ready')
                worker.ready.set_result(worker)

    async def before(self, inputs: dict) -> dict:
        await self.create_cluster(**inputs)
        return inputs

    async def run(self, workers: int = 5):
        print('~~ dask cluster running')
        self.running = True
        while self.running:
            await sleep(1)
        return 'ok'

    async def after(self, inputs: dict):
        await self.dask.close()

        print('~~ stopping dask cluster')
        self.scheduler.destroy()

        for worker in self.workers:
            worker.destroy()

        await super().after(inputs)

    async def create_cluster(self, workers=1) -> None:
        print('~~ creating dask cluster...')
        print(f'~~   workers = {workers}')

        # create dask scheduler
        self.scheduler = self.spawn(
            DaskScheduler,
            routes={
                # '/': 8787,
            },
        )
        self.scheduler.ready = Future()
        self.scheduler_uri = f'tcp://{self.scheduler.ip}:8786'

        await sleep(1)

        # create workers
        self.workers = []
        await self.add_workers(workers)

        print('~~ waiting for cluster nodes')
        await self.wait_for_nodes()

        print('~~ dask cluster ready')
        self.dask = DaskClient(address=self.scheduler_uri)

    async def add_workers(self, count):
        for i in range(0, count):
            w = DaskWorker(scheduler=self.scheduler_uri)
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
            asyncio.wrap_future(self.scheduler.ready),
            *map(lambda w: asyncio.wrap_future(w.ready), self.workers),
        )

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
    async def get_scheduler_uri(self) -> str:
        return self.scheduler_uri

    @rpc
    async def get_client(self) -> DaskClient:
        """ Returns a Dask client for this cluster """
        return self.dask

    @rpc
    async def teardown(self) -> None:
        self.running = False
