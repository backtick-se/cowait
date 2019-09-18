import os
import zmq
import json
import importlib
from typing import Dict, TypeVar
from pipeline.engine import ClusterProvider, TaskContext
from pipeline.utils.stream_capture import StreamCapturing

def load_task_class(task_name: str) -> TypeVar:
    module = importlib.import_module(task_name)
    print('module', module)

    try:
        task_class = getattr(module, 'Task')
        print('task', task_class)
        return task_class
    except AttributeError:
        raise RuntimeError('No task class exported from module')


class TaskExecutor(object):
    def execute(self):
        pass

class RootExecutor(TaskExecutor):
    def execute(self, context):
        context.send = self.handle_packet
        pass

    def handle_packet(self, data):
        msg = json.loads(data)
        if msg['type'] == 'log':
            print(msg['data'])
        if msg['type'] == 'status':
            print('~~ Task', msg['id'], 'changed status to', msg['status'])


def execute(task_name: str, provider: ClusterProvider, taskdef: Dict = { }) -> None:
    print('executing task:', task_name)

    # import task class
    TaskClass = load_task_class(task_name)

    # create task context
    context = TaskContext(
        cluster=provider,
        config=taskdef['config'],
    )
    context.id = taskdef['id']

    # task networking
    parent_host = os.environ['TASK_PARENT_HOST']
    root_task = parent_host == 'ROOT'
    if root_task:
        # root task has no parent connection
        # log output
        print('im the root task')

        def handle_packet(msg):
            if msg['type'] == 'return':
                print('~~ Task', msg['id'], 'returned:')
                print(json.dumps(msg['result'], indent=2))
            if msg['type'] == 'log':
                print(msg['data'], end='')
            if msg['type'] == 'status':
                print('~~ Task', msg['id'], 'changed status to', msg['status'])
            
        context.send = handle_packet
    else:
        # stream output to parent
        port = 1337
        mq = zmq.Context()
        parent = mq.socket(zmq.PUSH)
        
        parent.connect(f'tcp://{parent_host}:{port}')
        print('connected to parent', parent_host)
        
        context.send = parent.send_json

    def send(type, **kwargs):
        context.send({
            'id': taskdef['id'],
            'type': type,
            **kwargs,
        })

    # instantiate & run task
    send('status', status='run')

    if root_task:
        task = TaskClass()
        result = task.run(context, taskdef['inputs'])
    else:
        capturing = StreamCapturing(
            on_stdout=lambda data: send('log', file='stdout', data=data),
            on_stderr=lambda data: send('log', file='stderr', data=data),
        )
        with capturing:
            task = TaskClass()
            result = task.run(context, taskdef['inputs'])

    send('status', status='done')

    # submit result
    send('return', result=result)
