import inspect
from typing import Any
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


def spawn(*args, **kwargs):
    """Spawns subtasks from functional tasks. API is identical to Task.spawn()"""
    task = Task.get_current()
    if task is None:
        raise RuntimeError('No running task found')
    return task.spawn(*args, **kwargs)


def input(name: str, default: Any = None) -> Any:
    """Returns the value of an input to the currently running task"""
    task = Task.get_current()
    if task is None:
        raise RuntimeError('No running task found')

    if default is None and name not in task.taskdef.inputs:
        raise ValueError(f'Input {name} has no default value')

    return task.taskdef.inputs.get(name, default)


def exit(result: Any = None) -> None:
    """Exits the currently running task with the provided result"""
    task = Task.get_current()
    if task is None:
        raise RuntimeError('No running task found')
    task.exit(result)
