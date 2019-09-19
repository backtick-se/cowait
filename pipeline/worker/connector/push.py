from pipeline.network import PushSocket
from .connector import UpstreamConnector


class PushConnector(UpstreamConnector):
    """
    Connects tasks by pushing messages to an upstream Pull socket.

    Attributes:
        id (str): Local task id
        parent (PushSocket): Parent connection
    """

    def __init__(self, id: str, parent: str):
        """
        Create a new PushConnector.

        Arguments:
            id (str): Local task id
            parent (str): Parent connection string
        """
        super().__init__(id)
        self.parent = PushSocket(parent)


    def msg(self, type: str, **msg):
        # pass message to parent
        self.parent.send({
            'id': self.id,
            'type': type,
            **msg,
        })
