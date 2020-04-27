import json
from cowait.network import Conn
from cowait.tasks.messages import \
    TASK_INIT, TASK_STATUS, TASK_RETURN, TASK_FAIL, TASK_LOG


class TaskList(dict):
    """ In-memory database containing all seen tasks and logs """

    def __init__(self, task):
        task.node.children.on(TASK_INIT, self.on_init)
        task.node.children.on(TASK_STATUS, self.on_status)
        task.node.children.on(TASK_RETURN, self.on_return)
        task.node.children.on(TASK_FAIL, self.on_fail)
        task.node.children.on(TASK_LOG, self.on_log)

    async def on_init(self, conn: Conn, id: str, task: dict, **msg):
        print('~~ create', task['id'], 'from', task['image'], task['inputs'])
        self[id] = task

    async def on_status(self, conn: Conn, id, status, **msg):
        print('~~', id, 'changed status to', status)
        if id in self:
            self[id]['status'] = status

    async def on_fail(self, conn: Conn, id, error, **msg):
        print('~~', id, 'failed with error:')
        print(error.strip())
        if id in self:
            self[id]['error'] = error

    async def on_return(self, conn: Conn, id, result, **msg):
        print('~~', id, 'returned:')
        print(json.dumps(result, indent=2))
        if id in self:
            self[id]['result'] = result

    async def on_log(self, conn: Conn, id, file, data, **msg):
        if id in self:
            if 'log' not in self[id]:
                self[id]['log'] = ''
            self[id]['log'] += data
