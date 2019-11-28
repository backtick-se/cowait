import asyncio
from typing import Any
from .flow import Flow

# todo: refactor to websockets


class SparkFlow(Flow):
    async def run(self, workers=1, **inputs) -> Any:
        self.node.bind('tcp://*:1337')
        self.node.attach(self)

        # run task daemon in the background
        asyncio.create_task(self.node.serve())

        # build spark images on top of this one
        # FROM {self.context.image}
        # install spark

        # deploy
        self.task(
            name='master',
            image='spark-master',
            env={},
        )
        for i in range(0, workers):
            self.task(
                name=f'worker{i}',
                image='spark-worker',
                env={},
            )

        try:
            return await self.plan(**inputs)
        finally:
            self.stop()
