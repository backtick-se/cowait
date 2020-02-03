import asyncio
from pipeline.tasks import Task, sleep
from pipeline.network import Conn


class AgentTask(Task):
    async def before(self, inputs: dict) -> None:
        self.subscribers = []
        self.node.children.on('subscribe', self.subscribe)
        self.node.children.on('__close', self.unsubscribe)

        # forward any messages to subscribers
        self.node.children.on('*', self.forward)

        # run task daemon in the background
        asyncio.create_task(self.node.children.serve())

        # todo: api web server

        return inputs

    async def run(self, **inputs):
        # wait forever
        while True:
            await sleep(1.0)
        return {}

    async def forward(self, conn: Conn, **msg):
        if conn in self.subscribers:
            return

        for subscriber in self.subscribers:
            await subscriber.send(msg)

    async def subscribe(self, conn: Conn, **msg):
        print('added subscriber from', conn.ws.remote_address)
        self.subscribers.append(conn)
