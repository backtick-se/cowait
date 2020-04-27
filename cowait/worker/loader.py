import inspect
import importlib
from typing import TypeVar
from cowait.tasks import Task, TaskNotFoundError


def load_task_class(task_name: str) -> TypeVar:
    """
    Loads a task class from the given module.

    Arguments:
        task_name (str): Import path of the module containing the task.

    Raises:
        TaskNotFoundError

    Returns:
        Class (type)
    """

    def is_task(obj):
        """
        Predicate function which returns true for objects that are
        subclasses of Task and defined in the loaded module.
        """
        return inspect.isclass(obj) and \
            issubclass(obj, Task) and \
            obj.__module__.startswith(task_name)

    if task_name.startswith('.') or task_name.endswith('.'):
        raise TaskNotFoundError(f'Illegal task name {task_name}')

    try:
        module = importlib.import_module(task_name)
        classes = inspect.getmembers(module, is_task)

        # return an error if no tasks were found
        if len(classes) == 0:
            raise TaskNotFoundError(
                f'Module {task_name} does not contain any tasks')

        # each module should only define one task
        if len(classes) > 1:
            raise TaskNotFoundError(
                f'Module {task_name} contains multiple task definitions')

        # return task class
        _, Class = classes[0]
        return Class

    except ModuleNotFoundError:
        raise TaskNotFoundError(f'Task module {task_name} not found')
