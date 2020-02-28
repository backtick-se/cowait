import pytest
from .loader import load_task_class
from pipeline.tasks import Task, TaskNotFoundError
from pipeline.tasks.shell import ShellTask


class TaskOne(Task):
    pass


class TaskTwo(Task):
    pass


def test_illegal_class_name():
    with pytest.raises(TaskNotFoundError, match=r'.*Illegal.*'):
        load_task_class('pipeline.')

    with pytest.raises(TaskNotFoundError, match=r'.*Illegal.*'):
        load_task_class('.pipeline')


def test_load_task_class():
    loaded = load_task_class('pipeline.tasks.shell')
    assert loaded == ShellTask


def test_task_module_not_found():
    with pytest.raises(TaskNotFoundError):
        load_task_class('pipeline.worker.unknown_module')


def test_no_defined_tasks():
    with pytest.raises(TaskNotFoundError, match=r'.*not contain any tasks.*'):
        load_task_class('pipeline.worker.loader')


def test_multiple_defined_tasks():
    with pytest.raises(TaskNotFoundError, match=r'.*multiple*.'):
        load_task_class('pipeline.worker.test_loader')
