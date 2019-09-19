import importlib
from typing import TypeVar
from pipeline.tasks import TaskDefinition, TaskContext, TaskNotFoundError


def load_task_class(taskdef: TaskDefinition) -> TypeVar:
    try:
        module = importlib.import_module(taskdef.name)
        task_class = getattr(module, 'Task')
        return task_class

    except ModuleNotFoundError:
        raise TaskNotFoundError(f'No such task module: {taskdef.name}')

    except AttributeError:
        raise TaskNotFoundError(f'No task class exported from module {taskdef.name}')


def instantiate_task_class(taskdef: TaskDefinition, context: TaskContext):
    TaskClass = load_task_class(taskdef)
    return TaskClass(context)