import json
from .connector import UpstreamConnector


class LoggingConnector(UpstreamConnector):
    """
    Logs messages to stdout.
    Be careful not to use this while capturing stdout/stderr, as it will cause infinite recursion.
    """

    def __init__(self, id: str):
        """
        Arguments:
            id (str): Local task id
        """
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
            print(str(msg['error']).strip())

        elif type == 'init':
            task = msg['task']
            print('~~ Create', task['id'], 'from', task['image'], task['inputs'])

        elif type == 'status':
            print('~~', msg['id'], 'changed status to', msg['status'])

        elif type == 'log':
            print(msg['data'], end='')

        else:
            print(msg)
