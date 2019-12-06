import importlib
from typing import TypeVar
from pipeline.tasks import TaskNotFoundError


def load_task_class(task_name: str) -> TypeVar:
    try:
        module_name = task_name
        class_name = 'Task'

        if '.' in task_name:
            dot = task_name.rfind('.')
            module_name = task_name[:dot]
            class_name = task_name[dot+1:]

        module = importlib.import_module(module_name)
        task_class = getattr(module, class_name)

        return task_class

    except ModuleNotFoundError:
        raise TaskNotFoundError(f'No such task module: {task_name}')

    except AttributeError:
        raise TaskNotFoundError(
            f'No task class exported from module {task_name}')
