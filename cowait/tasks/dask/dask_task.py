from pipeline.tasks import Task
from dask.distributed import Client as DaskClient


class DaskTask(Task):
    async def before(self, inputs: dict) -> dict:
        if 'cluster' not in inputs:
            raise RuntimeError('Dask cluster info not found in inputs')

        scheduler = inputs.get('cluster').get('scheduler')
        dask = DaskClient(address=scheduler)

        print('~~ starting dask session')
        inputs['dask'] = dask

        return inputs
