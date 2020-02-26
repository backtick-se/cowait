import json
from pipeline.network import Conn


class TaskList(object):
    def __init__(self, task):
        self.tasks = {}

        task.node.children.on('init', self.on_init)
        task.node.children.on('status', self.on_status)
        task.node.children.on('return', self.on_return)
        task.node.children.on('fail', self.on_fail)
        task.node.children.on('log', self.on_log)

    def get(self, id):
        return self.tasks[id]

    def values(self):
        return self.tasks.values()

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
