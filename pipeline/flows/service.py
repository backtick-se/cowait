import json
import traceback

class FlowService(object):
    def handle(self, id: str, type: str, **msg):
        if   type == 'init':   self.on_init(msg['task'])
        elif type == 'fail':   self.on_fail(id, msg['error'])
        elif type == 'return': self.on_return(id, msg['result'])
        elif type == 'status': self.on_status(id, msg['status'])
        elif type == 'log':    self.on_log(id, msg['file'], msg['data'])
        else:
            raise RuntimeError('error parsing message: %s\n%s\n%s' % (
                type, 
                traceback.format_exc(), 
                json.dumps(msg))
            )

    def on_init(self, task: dict):
        pass

    def on_status(self, id, status):
        pass

    def on_fail(self, id, error):
        pass

    def on_return(self, id, result):
        pass

    def on_log(self, id, file, data):
        pass


class FlowLogger(FlowService):
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