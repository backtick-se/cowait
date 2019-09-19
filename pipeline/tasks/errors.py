

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


class ReturnException(Exception):
    """ Raised to return from a flow message loop """
    pass


class StopException(Exception):
    """ Raised to abort task execution """
    pass
