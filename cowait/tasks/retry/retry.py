from cowait import Task


class RetryTask(Task):
    async def run(self, taskdef, retries: int = 3):
        for i in range(retries):
            try:
                return await self.spawn(**taskdef)

            except Exception as e:
                print('Retry', i, 'failed:', str(e))

        raise Exception('Task execution failed after', retries, 'retries.')
