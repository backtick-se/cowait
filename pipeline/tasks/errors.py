

class TaskError(RuntimeError):
    def __init__(self, error):
        self.error = error


class ReturnException(RuntimeError):
    pass
