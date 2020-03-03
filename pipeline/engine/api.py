import aiohttp
import asyncio
import requests
import traceback
from threading import Thread
from queue import Queue, Empty as QueueEmpty
from pipeline.tasks.messages import TASK_FAIL, TASK_RETURN, TASK_LOG
from pipeline.tasks import TaskDefinition, RemoteTask
from .cluster import ClusterProvider


class ApiProvider(ClusterProvider):
    def __init__(self, args={}):
        super().__init__('api', args)
        self.url = args.get('url')

    def rpc(self, method: str, **kwargs) -> dict:
        # todo: authentication
        url = f'{self.url}/rpc/{method}'
        resp = requests.post(url, json=kwargs)
        msg = resp.json()
        if resp.status_code == 200:
            return msg
        if resp.status_code == 400 and 'error' in msg:
            raise RuntimeError(msg['error'])
        raise RuntimeError(f'Request status {resp.status_code}')

    def spawn(self, taskdef: TaskDefinition) -> RemoteTask:
        task = self.rpc('spawn', **taskdef.serialize())
        return RemoteTask(TaskDefinition.deserialize(task), self)

    def destroy(self, task_id):
        self.rpc('destroy', task_id=task_id)

    def destroy_all(self):
        self.rpc('destroy_all')

    def list_all(self):
        return self.rpc('list_tasks')

    def logs(self, task):
        ws_url = self.args.get('ws_url')

        watcher = ApiLogsWatcher(task.id, ws_url)
        for log in watcher.watch():
            yield log


class ApiLogsWatcher(Thread):
    END = object()

    def __init__(self, task_id, ws_url):
        super().__init__()
        self.task_id = task_id
        self.ws_url = ws_url
        self.queue = Queue()

    def run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.__watch())

    def watch(self, timeout=60):
        self.start()
        while True:
            try:
                log = self.queue.get(True, timeout)
                if log is self.END:
                    break
                yield log
            except QueueEmpty:
                break

    async def __watch(self):
        try:
            session = aiohttp.ClientSession()
            ws = await session.ws_connect(self.ws_url)
            await ws.send_json({
                'type': 'subscribe'
            })
            while True:
                msg = await ws.receive()
                if msg.type == aiohttp.WSMsgType.CLOSE:
                    self.queue.put('!! Lost API connection')
                    break
                if msg.type == aiohttp.WSMsgType.ERROR:
                    self.queue.put('!! Lost API connection')
                    break

                event = msg.json()
                if 'id' not in event or event['id'] != self.task_id:
                    continue
                if event['type'] == TASK_RETURN:
                    break
                if event['type'] == TASK_FAIL:
                    self.queue.put(f'!! {self.task_id} failed with error:')
                    self.queue.put(event['error'].strip())
                    break
                if event['type'] == TASK_LOG:
                    self.queue.put(event['data'].strip())

        except Exception:
            traceback.print_exc()
        finally:
            await ws.close()
            await session.close()

        self.queue.put(self.END)
