import zmq

class PushSocket(object):
    """ Thin wrapper over a ZeroMQ push socket """

    def __init__(self, target):
        self.target = target
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect(target)


    def send(self, data: dict) -> None:
        return self.socket.send_json(data)
