Module cowait.tasks.errors
==========================

Classes
-------

`StoppedError(*args, **kwargs)`
:   Unspecified run-time error.

    ### Ancestors (in MRO)

    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException

`TaskError(error: str)`
:   Raised when an error is received from a subtask
    
    Attributes:
        error (str): Original error message
    
    Arguments:
        error (str): Original error message

    ### Ancestors (in MRO)

    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException

`TaskNotFoundError(*args, **kwargs)`
:   Raised when a task can not be instantiated

    ### Ancestors (in MRO)

    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException