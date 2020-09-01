from cowait.tasks.shell import ShellTask


class SparkWorker(ShellTask):
    async def run(self, master: str, cores: int = 2, memory = '4G') -> dict:
        return await super().run(
            command=' '.join([
                'spark-class',
                'org.apache.spark.deploy.worker.Worker',
                master,
            ]),
            env={
                'SPARK_WORKER_CORES': str(cores),
                'SPARK_WORKER_MEMORY': memory,
            },
        )
