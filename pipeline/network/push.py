import zmq

class PushSocket(object):
    def __init__(self, target):
        self.target = target
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect(target)


    def send(self, data: dict) -> None:
        return self.socket.send_json(data)


    def close(self) -> None:
        self.socket.close()

    
    def __del__(self) -> None:
        self.close()