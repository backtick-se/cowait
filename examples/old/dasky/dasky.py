from pipeline.tasks.dask import DaskCluster


class DaskyTask(DaskCluster):
    async def run(
        self,
        dask,
        **inputs,
    ):
        print('hello dask')
