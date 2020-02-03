from aiohttp import web


class TaskAPI(object):
    def __init__(self, agent):
        self.agent = agent
        self.tasks = agent.tasks

    def routes(self, path: str = 'tasks'):
        return [
            web.post(path, self.create_task),
            web.get(path, self.get_tasks),
            web.get('%s/{id}' % path, self.get_task),
        ]

    async def get_tasks(self, req):
        tasks = list(self.tasks.values())
        return web.json_response(tasks)

    async def get_task(self, req):
        id = req.match_info['id']
        task = self.tasks.get(id)
        return web.json_response(task)

    async def create_task(self, req):
        taskdef = await req.json()
        task = self.agent.spawn(**taskdef)
        return web.json_response(task.serialize())
