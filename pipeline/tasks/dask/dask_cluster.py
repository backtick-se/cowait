import asyncio
from pipeline.tasks import Task, sleep
from pipeline.tasks.messages import TASK_LOG
from concurrent.futures import Future
from dask.distributed import Client as DaskClient

MSG_LEADER = 'Scheduler at:'
MSG_REGISTER = 'Registered to:'


class DaskCluster(Task):
    def init(self):
        self.scheduler = None
        self.workers = []
        self.dask_cluster = {}

        # subscribe to logs
        self.node.children.on(TASK_LOG, self.on_log)

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
        await self.create_cluster()

        self.dask = DaskClient(address=self.dask_cluster['scheduler'])

        print('~~ starting dask session')
        inputs['dask'] = self.dask

        return inputs

    async def after(self, inputs: dict):
        self.dask.close()

        print('~~ destroying dask cluster')
        await self.scheduler.stop()
        for worker in self.workers:
            await worker.stop()

        await super().after(inputs)

    async def create_cluster(self, num_workers=2) -> None:
        print(f'~~ creating dask cluster...')
        print(f'~~   num_workers = {num_workers}')

        # create dask scheduler
        self.scheduler = self.spawn(
            name='pipeline.tasks.shell',
            command='dask-scheduler',
            image='backtickse/task',
            routes={
                # '/': 8787,
            },
        )
        self.scheduler.ready = Future()
        scheduler_uri = f'tcp://{self.scheduler.ip}:8786'

        await sleep(1)
        self.dask_cluster = {
            'scheduler': scheduler_uri,
        }

        # create workers
        self.workers = []
        await self.add_workers(num_workers)

        print('~~ waiting for cluster nodes')
        await self.wait_for_nodes()

        print('~~ dask cluster ready')

    async def add_workers(self, count):
        command = 'dask-worker ' + self.dask_cluster['scheduler']
        for i in range(0, count):
            w = self.spawn(
                name='pipeline.tasks.shell',
                image='backtickse/task',
                command=command,
            )
            w.ready = Future()
            self.workers.append(w)

    async def wait_for_nodes(self):
        await asyncio.gather(
            asyncio.wrap_future(self.scheduler.ready),
            *map(lambda w: asyncio.wrap_future(w.ready), self.workers),
        )

    def spawn(
        self,
        name: str,
        image: str = None,
        env: dict = {},
        **inputs,
    ) -> Task:
        return super().spawn(
            name=name,
            image=image,
            env=env,
            **inputs,
            dask=self.dask_cluster,
        )
