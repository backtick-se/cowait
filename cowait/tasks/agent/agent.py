from datetime import datetime, timezone
from cowait.tasks import Task, TaskDefinition, sleep, rpc
from cowait.network import Conn, get_local_url
from cowait.tasks.status import WAIT, WORK, STOP
from cowait.tasks.messages import TASK_INIT, TASK_STATUS
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
                    'id':   task.id,
                    'task': task.serialize(),
                })
        self.subs.on('subscribe', send_state)

        self.token = self.meta['http_token']
        if self.token is None or self.token == '':
            self.node.server.auth.enabled = False
            self.token = 'none'

        # create http server
        self.node.server.add_routes(TaskAPI(self).routes('/api/1/tasks'))
        self.node.server.add_routes(Dashboard().routes())
        self.node.server.auth.add_token(self.token)

    async def run(self, **inputs) -> dict:
        if '/' in self.taskdef.routes:
            url = self.taskdef.routes['/']['url']
            print('Agent ready. Dashboard available at:')
            print(f'{url}?token={self.token}')
        else:
            print('Warning: No route set for /, dashboard not available.')

        # monitor tasks
        while True:
            running_tasks = self.cluster.list_all()
            for id, task in self.tasks.items():
                # consider only tasks that are waiting or running
                if task.status != WAIT and task.status != WORK:
                    continue

                # check if parent is dead
                if task.parent is not None and task.parent not in running_tasks:
                    parent = self.tasks[task.parent]
                    virtual_parent = parent.meta.get('virtual', False)
                    if not virtual_parent or parent.status != WORK:
                        since = datetime.now(timezone.utc) - task.created_at
                        await self.subtasks.emit_child_error(id, f'Task lost parent after {since}')

                        # destroy it
                        self.cluster.destroy(task.id)

                # special case for virtual tasks: since they dont exist as containers,
                # we cant check if they are still alive.
                if task.meta.get('virtual', False):
                    continue

                # ensure task is still in the list of running tasks
                # if not, consider it lost.
                if id not in running_tasks:
                    # compute task age
                    since = datetime.now(timezone.utc) - task.created_at
                    error = f'Task lost after {since}'
                    await self.subtasks.emit_child_error(id, error)

            await sleep(5.0)

        return {}

    @rpc
    async def destroy(self, task_id) -> None:
        await self.emulate_stop(task_id)
        self.cluster.destroy(task_id)

    @rpc
    async def destroy_all(self) -> None:
        for id, task in self.tasks.items():
            if task.status == WAIT or task.status == WORK:
                await self.emulate_stop(id)
        self.cluster.destroy_all()

    @rpc
    async def list_tasks(self) -> list:
        return self.cluster.list_all()

    @rpc
    async def get_agent_url(self) -> str:
        url = get_local_url()
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
    ) -> dict:
        if not isinstance(name, str) and issubclass(name, Task):
            name = name.__module__

        # todo: throw error if any input is a coroutine

        task = self.cluster.spawn(TaskDefinition(
            id=id,
            name=name,
            image=image,
            upstream=get_local_url(),
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
        self.node.server.auth.add_token(id)

        # register with subtask manager
        self.subtasks.watch(task)

        return task.serialize()

    async def emulate_stop(self, task_id: str):
        await self.node.server.emit(type=TASK_STATUS, id=task_id, status=STOP, conn=None)
