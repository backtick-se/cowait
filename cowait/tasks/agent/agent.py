from cowait.tasks import Task, TaskDefinition, sleep, rpc
from cowait.network import Conn, get_local_connstr
from cowait.tasks.messages import TASK_INIT
from .tasklist import TaskList
from .subscriptions import Subscriptions
from .api import Dashboard, TaskAPI


class Agent(Task):
    def init(self):
        self.tasks = TaskList(self)
        self.subs = Subscriptions(self)

        # subscriber events
        async def send_state(conn: Conn) -> None:
            """" sends the state of all known tasks """
            for task in self.tasks.values():
                await conn.send({
                    'type': TASK_INIT,
                    'id':   task['id'],
                    'task': task,
                })
        self.subs.on('subscribe', send_state)

        self.token = self.meta['http_token']

        # create http server
        self.node.http.add_routes(TaskAPI(self).routes('/api/1/tasks'))
        self.node.http.add_routes(Dashboard().routes())
        self.node.http.auth.add_token(self.token)

    async def run(self, **inputs):
        url = self.routes['/']['url']
        print('agent ready. available at:')
        print(f'{url}?token={self.token}')

        # wait forever
        while True:
            await sleep(1.0)
        return {}

    @rpc
    async def destroy(self, task_id):
        self.cluster.destroy(task_id)

    @rpc
    async def destroy_all(self):
        self.cluster.destroy_all()

    @rpc
    async def list_tasks(self):
        return self.cluster.list_all()

    @rpc
    async def get_agent_url(self):
        url = get_local_connstr()
        return f'{url}?token={self.token}'

    @rpc
    async def spawn(
        self,
        name: str,
        image: str,
        id: str = None,
        ports: dict = {},
        routes: dict = {},
        inputs: dict = {},
        meta: dict = {},
        env: dict = {},
        cpu: str = '0',
        memory: str = '0',
        owner: str = '',
        **kwargs: dict,
    ) -> Task:
        if not isinstance(name, str) and issubclass(name, Task):
            name = name.__module__

        # todo: throw error if any input is a coroutine

        task = self.cluster.spawn(TaskDefinition(
            id=id,
            name=name,
            image=image,
            upstream=get_local_connstr(),
            meta=meta,
            ports=ports,
            routes=routes,
            env=env,
            cpu=cpu,
            memory=memory,
            owner=owner,
            inputs={
                **inputs,
                **kwargs,
            },
        ))

        # authorize id
        self.node.http.auth.add_token(id)

        # register with subtask manager
        self.subtasks.watch(task)

        return task.serialize()
