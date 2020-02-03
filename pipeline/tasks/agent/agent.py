import json
import asyncio
from pipeline.tasks import Task, sleep
from pipeline.network import Conn


class AgentTask(Task):
    async def before(self, inputs: dict) -> None:
        self.tasks = {}
        self.subscribers = []
        self.node.children.on('subscribe', self.subscribe)
        self.node.children.on('__close', self.unsubscribe)

        # forward any messages to subscribers
        self.node.children.on('*', self.forward)

        self.node.children.on('init', self.on_init)
        self.node.children.on('status', self.on_status)
        self.node.children.on('return', self.on_return)
        self.node.children.on('fail', self.on_fail)
        self.node.children.on('log', self.on_log)

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
        print(f'~~ add subscriber {conn.remote_ip}:{conn.remote_port}')
        self.subscribers.append(conn)

        # send task info
        for task in self.tasks.values():
            await conn.send({
                'id': task['id'],
                'type': 'init',
                'task': task,
            })

    async def unsubscribe(self, conn: Conn, **msg):
        print(f'~~ drop subscriber {conn.remote_ip}:{conn.remote_port}')
        if conn in self.subscribers:
            self.subscribers.remove(conn)

    async def on_init(self, conn: Conn, id: str, task: dict, **msg):
        print('~~ create', task['id'], 'from', task['image'], task['inputs'])
        self.tasks[id] = task

    async def on_status(self, conn: Conn, id, status, **msg):
        print('~~', id, 'changed status to', status)
        if id in self.tasks:
            self.tasks[id]['status'] = status

    async def on_fail(self, conn: Conn, id, error, **msg):
        print('~~', id, 'failed with error:')
        print(error.strip())
        if id in self.tasks:
            self.tasks[id]['error'] = error

    async def on_return(self, conn: Conn, id, result, **msg):
        print('~~', id, 'returned:')
        print(json.dumps(result, indent=2))
        if id in self.tasks:
            self.tasks[id]['result'] = result

    async def on_log(self, conn: Conn, id, file, data, **msg):
        if id in self.tasks:
            if 'log' not in self.tasks[id]:
                self.tasks[id]['log'] = ''
            self.tasks[id]['log'] += data
