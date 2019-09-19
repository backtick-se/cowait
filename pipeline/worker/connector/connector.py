from abc import ABC, abstractmethod


class WorkerConnector(ABC):
    def __init__(self, id):
        super().__init__()
        self.id = id


    @abstractmethod
    def msg(self, type: str, **msg):
        pass


    def init(self, taskdef):
        self.msg('init', task=taskdef.serialize())


    def run(self):
        self.msg('status', status='run')


    def done(self, result):
        self.msg('status', status='done')
        self.msg('return', result=result)


    def fail(self, error):
        self.msg('status', status='error')
        self.msg('fail',   error=error)


    def log(self, file, data):
        self.msg('log', file=file, data=data)
