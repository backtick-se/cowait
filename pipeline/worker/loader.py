import importlib
from typing import TypeVar
from pipeline.tasks import TaskNotFoundError


def load_task_class(task_name: str) -> TypeVar:
    try:
        module_name = task_name
        class_name = 'Task'

        if '.' in task_name:
            # make sure the task name does not end with a dot
            dot = task_name.rfind('.')
            if dot == 0 or dot == len(task_name)-1:
                raise TaskNotFoundError(f'Illegal task name: {task_name}')

            if task_name[dot+1].isupper():
                # if the first character after the last dot is uppercase,
                # consider it a class name.
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
