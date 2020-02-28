from pipeline.tasks import Task, TaskDefinition, sleep
from pipeline.network import Conn, get_local_connstr
from pipeline.tasks.components import HttpComponent
from pipeline.tasks.messages import TASK_INIT
from .tasklist import TaskList
from .subscriptions import Subscriptions
from .api import Dashboard, TaskAPI


class Agent(Task):
    async def before(self, inputs: dict) -> None:
        self.tasks = TaskList(self)
        self.subs = Subscriptions(self)

        # subscriber events
        async def send_state(conn: Conn) -> None:
            """" sends the state of all known tasks """
            for task in self.tasks.values():
                await conn.send({
                    'type': TASK_INIT,
                    'id': task['id'],
                    'task': task,
                })
        self.subs.on('subscribe', send_state)

        # create http server
        self.http = HttpComponent(self)
        self.http.add_routes(TaskAPI(self).routes('/api/1/tasks'))
        self.http.add_routes(Dashboard().routes())

        self.http.start()
        return inputs

    async def run(self, **inputs):
        print('agent ready. available at:')
        print(self.routes['/']['url'])

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
