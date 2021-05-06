import json


class StoppedError(RuntimeError):
    def __init__(self, result):
        super().__init__('Exited')
        self.result = result

    def _render_traceback_(self):
        try:
            return ['Returned with result:'] + json.dumps(self.result, indent=2).split('\n')
        except TypeError:
            return ['Returned with result:', str(self.result)]


class TaskError(RuntimeError):
    """
    Raised when an error is received from a subtask

    Attributes:
        error (str): Original error message
    """

    def __init__(self, error: str):
        """
        Arguments:
            error (str): Original error message
        """
        self.error = error


class TaskNotFoundError(RuntimeError):
    """ Raised when a task can not be instantiated """
    pass
