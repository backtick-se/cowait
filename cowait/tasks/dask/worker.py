from cowait.tasks.shell import ShellTask


class DaskWorker(ShellTask):
    async def before(self, inputs):
        scheduler = inputs['scheduler']
        inputs['command'] = f'dask-worker {scheduler}'
        return inputs
