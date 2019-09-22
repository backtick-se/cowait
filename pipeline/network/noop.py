

class NoopSocket(object):
    """ The NoOp socket discards everything sent to it. """

    def send(self, data) -> None:
        pass
