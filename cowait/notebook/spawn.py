import dill
import base64
from cowait.tasks import TaskDefinition
from cowait.network import get_local_connstr
from cowait.worker import env_get_cluster_provider, env_get_task_definition

cluster = env_get_cluster_provider()
taskdef = env_get_task_definition()


def spawn(task: str, env: dict = {}, **inputs):
    if callable(task):
        # serialize function and return it as a base64 string
        inputs['func'] = str(base64.b64encode(dill.dumps(task)), encoding='utf-8')
        task = 'cowait.tasks.pickled'

    task = cluster.spawn(TaskDefinition(
        name=task,
        image=taskdef.image,
        parent=taskdef.id,
        upstream=get_local_connstr(),
        inputs=inputs,
        env=env,
    ))
    return HtmlLogs([m for m in task.logs()])


def task(task_func):
    def spawn_task(*args, **inputs):
        if len(args) > 0:
            raise TypeError('Use keyword arguments for task inputs')
        return spawn(task_func, **inputs)
    return spawn_task


class HtmlLogs(object):
    def __init__(self, log):
        self.items = log

    def _repr_html_(self):
        html = ''
        for msg in self.items:
            if msg.get('type', '') == 'task/log':
                html += msg.get('data').replace('\n', '<br>')
        return html
