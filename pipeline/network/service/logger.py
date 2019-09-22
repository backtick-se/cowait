import json
from .service import NodeService


class FlowLogger(NodeService):
    def on_init(self, task: dict):
        print('~~ Create', task['id'], 'from', task['image'], task['inputs'])

    def on_status(self, id, status):
        print('~~', id, 'changed status to', status)

    def on_fail(self, id, error):
        print('-- TASK FAILED: -------------------------------------')
        print('~~', id, 'failed with error:')
        print(error.strip())

    def on_return(self, id, result):
        print('~~', id, 'returned:')
        print(json.dumps(result, indent=2))

    def on_log(self, id, file, data):
        print(data, end='')
