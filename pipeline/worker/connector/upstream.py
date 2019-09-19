from pipeline.network import PushSocket
from .connector import WorkerConnector


class UpstreamConnector(WorkerConnector):
    """
    Pushes messages to an upstream Pull socket.
    """

    def __init__(self, id, parent):
        super().__init__(id)
        self.parent = PushSocket(f'tcp://{parent}:1337')


    def msg(self, type: str, **msg):
        self.parent.send({
            'id': self.id,
            'type': type,
            **msg,
        })
