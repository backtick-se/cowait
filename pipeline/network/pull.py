import zmq

class PullSocket(object):
    """ Thin wrapper over a ZeroMQ pull socket """

    def __init__(self, bind = None):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        if bind:
            self.bind(bind)


    def bind(self, bind):
        self.socket.bind(bind)


    def recv(self) -> dict:
        return self.socket.recv_json()
