import requests
from pipeline.tasks import TaskDefinition, RemoteTask
from .cluster import ClusterProvider


class ApiProvider(ClusterProvider):
    def __init__(self, args={}):
        super().__init__('api', args)
        self.url = args.get('url')

    def rpc(self, method: str, args: dict = {}) -> dict:
        # todo: authentication
        url = f'{self.url}/rpc/{method}'
        resp = requests.post(url, json=args)
        return resp.json()

    def spawn(self, taskdef: TaskDefinition) -> RemoteTask:
        task = self.rpc('spawn', taskdef.serialize())
        return RemoteTask(task, self)

    def destroy(self, task_id):
        self.rpc('destroy', task_id=task_id)

    def destroy_all(self):
        self.rpc('destroy_all')

    def list_all(self):
        return self.rpc('list_tasks')

    def logs(self, task):
        # can this be implemented without using async stuff?
        # could change the ClusterProvider.logs() function to async
        # subscribe to websocket, print logs
        return [
            'Real-time logs are not available when using the API provider',
        ]
