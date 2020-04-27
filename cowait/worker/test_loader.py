import pytest
from .loader import load_task_class
from cowait.tasks import Task, TaskNotFoundError
from cowait.tasks.shell import ShellTask


class TaskOne(Task):
    pass


class TaskTwo(Task):
    pass


def test_illegal_class_name():
    with pytest.raises(TaskNotFoundError, match=r'.*Illegal.*'):
        load_task_class('cowait.')

    with pytest.raises(TaskNotFoundError, match=r'.*Illegal.*'):
        load_task_class('.cowait')


def test_load_task_class():
    loaded = load_task_class('cowait.tasks.shell')
    assert loaded == ShellTask


def test_task_module_not_found():
    with pytest.raises(TaskNotFoundError):
        load_task_class('cowait.worker.unknown_module')


def test_no_defined_tasks():
    with pytest.raises(TaskNotFoundError, match=r'.*not contain any tasks.*'):
        load_task_class('cowait.worker.loader')


def test_multiple_defined_tasks():
    with pytest.raises(TaskNotFoundError, match=r'.*multiple*.'):
        load_task_class('cowait.worker.test_loader')
