import inspect
import importlib
from typing import TypeVar
from pipeline.tasks import Task, TaskNotFoundError


def load_task_class(task_name: str) -> TypeVar:
    def is_task(obj):
        return inspect.isclass(obj) and \
            issubclass(obj, Task) and \
            obj.__module__ == task_name

    try:
        module_name = task_name
        module = importlib.import_module(module_name)
        classes = inspect.getmembers(module, is_task)

        print(classes)
        for name, obj in classes:
            print(name, obj.__module__)

        if len(classes) > 1:
            raise TaskNotFoundError('Multiple tasks defined')

        if len(classes) == 0:
            raise TaskNotFoundError(
                f'Module {module_name} does not contain any tasks')

        return classes[0][1]

    except ModuleNotFoundError:
        raise TaskNotFoundError(f'Task module {task_name} not found')
