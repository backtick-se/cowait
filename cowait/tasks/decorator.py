from .task import Task


def task(func):
    """ Wraps a task function in a Task class """

    if func.__name__[0].lower() == func.__name__[0]:
        raise NameError(
            f'Task names must start with an uppercase character, '
            f'found {func.__name__}')

    class FuncTask(Task):
        run = func

    # copy name & module
    FuncTask.__name__ = func.__name__
    FuncTask.__module__ = func.__module__

    return FuncTask
