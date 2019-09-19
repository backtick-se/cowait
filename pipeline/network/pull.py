import zmq

class PullSocket(object):
    """ Thin wrapper over a ZeroMQ pull socket """

    def __init__(self, bind):
        self.bind = bind
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind(bind)


    def recv(self) -> dict:
        return self.socket.recv_json()
