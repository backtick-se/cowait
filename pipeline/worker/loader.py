import importlib
from typing import TypeVar
from pipeline.tasks import TaskNotFoundError


def load_task_class(task_name: str) -> TypeVar:
    try:
        module = importlib.import_module(task_name)
        task_class = getattr(module, 'Task')
        return task_class

    except ModuleNotFoundError:
        raise TaskNotFoundError(f'No such task module: {task_name}')

    except AttributeError:
        raise TaskNotFoundError(
            f'No task class exported from module {task_name}')
