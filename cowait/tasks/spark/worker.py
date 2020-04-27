from cowait.tasks.shell import ShellTask


class SparkWorker(ShellTask):
    async def before(self, inputs: dict) -> dict:
        if 'master' not in inputs:
            raise RuntimeError('Undefined input "master": expected master uri')

        master_uri = inputs.get('master')
        inputs['command'] = ' '.join([
            'spark-class',
            'org.apache.spark.deploy.worker.Worker',
            master_uri,
        ])

        return inputs
