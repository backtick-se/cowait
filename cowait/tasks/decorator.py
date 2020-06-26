import inspect
from .task import Task


def task(func):
    """ Wraps a task function in a Task class """

    if func.__name__[0].lower() == func.__name__[0]:
        raise NameError(
            f'Task names must start with an uppercase character, '
            f'found {func.__name__}')

    class FuncTask(Task):
        async def run(self, **inputs):
            if inspect.iscoroutinefunction(func):
                return await func(**inputs)
            else:
                return func(**inputs)

    # copy name & module
    FuncTask.__name__ = func.__name__
    FuncTask.__module__ = func.__module__
    FuncTask.__wraps__ = func

    return FuncTask
