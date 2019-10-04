import zmq
import zmq.asyncio

class PullSocket(object):
    """ Thin wrapper over a ZeroMQ pull socket """

    def __init__(self, bind = None):
        self.context = zmq.asyncio.Context()
        self.socket = self.context.socket(zmq.PULL)
        if bind:
            self.bind(bind)


    def bind(self, bind):
        self.socket.bind(bind)


    async def recv(self) -> dict:
        return await self.socket.recv_json()
