import json
from .connector import WorkerConnector


class LoggingConnector(WorkerConnector):
    """
    Logs messages to stdout.
    """

    def __init__(self, id):
        super().__init__(id)


    def msg(self, type: str, **msg):
        if not 'id' in msg:
            msg['id'] = self.id

        if type == 'return':
            print('~~', msg['id'], 'returned:')
            print(json.dumps(msg['result'], indent=2))
        elif type == 'fail':
            print('-- TASK FAILED: -------------------------------------')
            print('~~', msg['id'], 'failed with error:')
            print('>', self.id)
            print(str(msg['error']).strip())
        elif type == 'log':
            print(msg['data'], end='')
        elif type == 'init':
            task = msg['task']
            print('~~ Create', task['id'], 'from', task['image'], task['inputs'])
        elif type == 'status':
            print('~~', msg['id'], 'changed status to', msg['status'])
        else:
            print(msg)
