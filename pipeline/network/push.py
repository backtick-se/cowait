import zmq

class PushSocket(object):
    """ Thin wrapper over a ZeroMQ push socket """

    def __init__(self, target = None):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        if target:
            self.connect(target)


    def connect(self, target):
        self.socket.connect(target)


    def send(self, data: dict) -> None:
        return self.socket.send_json(data)
