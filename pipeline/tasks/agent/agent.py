from aiohttp import web
from pipeline.tasks import Task, TaskDefinition, sleep
from pipeline.network import Conn, get_local_connstr
from .tasklist import TaskList
from .subscriptions import Subscriptions
from .api import Dashboard, TaskAPI


class Agent(Task):
    async def before(self, inputs: dict) -> None:
        self.tasks = TaskList()
        self.subs = Subscriptions()

        async def send_state(conn: Conn) -> None:
            for task in self.tasks.values():
                await conn.send({
                    'type': 'init',
                    'id': task['id'],
                    'task': task,
                })

        # subscriber events
        self.node.children.on('subscribe', self.subs.subscribe)
        self.node.children.on('__close', self.subs.unsubscribe)
        self.node.children.on('*', self.subs.forward)
        self.subs.on('subscribe', send_state)

        # task events
        self.node.children.on('init', self.tasks.on_init)
        self.node.children.on('status', self.tasks.on_status)
        self.node.children.on('return', self.tasks.on_return)
        self.node.children.on('fail', self.tasks.on_fail)
        self.node.children.on('log', self.tasks.on_log)

        # run task websocket coroutine on io thread
        self.node.io.create_task(self.node.children.serve())

        app = web.Application()
        app.add_routes(TaskAPI(self).routes('/api/1/tasks'))
        app.add_routes(Dashboard().routes())

        # run web server coroutine on io thread
        self.node.io.create_task(web._run_app(
            app=app,
            port=1338,
            print=False,
            handle_signals=False,
        ))

        return inputs

    async def run(self, **inputs):
        # wait forever
        while True:
            await sleep(1.0)
        return {}

    def spawn(self,
              name: str,
              image: str = None,
              inputs: dict = {},
              config: dict = {},
              ports: dict = {},
              env: dict = {},
              ) -> TaskDefinition:
        taskdef = TaskDefinition(
            name=name,
            inputs=inputs,
            image=image if image else self.image,
            upstream=get_local_connstr(),
            config=config,
            ports=ports,
            env=env,
        )

        self.cluster.spawn(taskdef)
        return taskdef
