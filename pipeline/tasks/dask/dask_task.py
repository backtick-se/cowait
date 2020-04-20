from pipeline.tasks import Task
from dask.distributed import Client as DaskClient


class DaskTask(Task):
    async def before(self, inputs: dict) -> dict:
        if 'scheduler' not in inputs:
            raise RuntimeError('Dask scheduler URI not found in input')

        scheduler = inputs.get('scheduler')
        dask = DaskClient(address=scheduler)

        print('~~ starting dask session')
        inputs['dask'] = dask

        return inputs
