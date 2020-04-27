from cowait.tasks.shell import ShellTask


class SparkMaster(ShellTask):
    async def before(self, inputs: dict) -> dict:
        inputs['command'] = ' '.join([
            'spark-class',
            'org.apache.spark.deploy.master.Master',
        ])
        return inputs
