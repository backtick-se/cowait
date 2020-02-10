import inspect
import importlib
from typing import TypeVar
from pipeline.tasks import Task, TaskNotFoundError


def load_task_class(task_name: str) -> TypeVar:
    def is_task(obj):
        return inspect.isclass(obj) and \
            issubclass(obj, Task) and \
            obj.__module__.startswith(task_name)

    try:
        module = importlib.import_module(task_name)
        classes = inspect.getmembers(module, is_task)

        if len(classes) > 1:
            raise TaskNotFoundError('Multiple tasks defined')

        if len(classes) == 0:
            raise TaskNotFoundError(
                f'Module {task_name} does not contain any tasks')

        _, Class = classes[0]
        return Class

    except ModuleNotFoundError:
        raise TaskNotFoundError(f'Task module {task_name} not found')
