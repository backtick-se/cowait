from pipeline.network import PullSocket, PORT


class FlowServer(object):
    """ Downstream Server """

    def __init__(self, port, forwards = [ ]):
        self.daemon = PullSocket(f'tcp://*:{PORT}')
        self.listeners = list(forwards)


    def recv(self):
        msg = self.daemon.recv()
        self.handle(msg)
        return msg


    def handle(self, msg):
        for listener in self.listeners:
            listener(**msg)


    def listen(self, listener: callable):
        while True:
            msg = self.recv()
            listener(**msg) 


    def attach(self, listener: callable):
        self.listeners.append(listener)


    def detach(self, listener: callable):
        self.listeners.remove(listener)
