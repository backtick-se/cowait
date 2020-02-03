import pytest
from .loader import load_task_class
from pipeline.tasks import TaskNotFoundError


class CustomNameTask(object):
    pass


class Task(object):
    pass


def test_illegal_class_name():
    with pytest.raises(TaskNotFoundError):
        load_task_class('pipeline.')

    with pytest.raises(TaskNotFoundError):
        load_task_class('.pipeline')


def test_load_task_class():
    loaded = load_task_class('pipeline.worker.test_loader')
    assert loaded == Task


def test_load_task_custom_name():
    loaded = load_task_class('pipeline.worker.test_loader.CustomNameTask')
    assert loaded == CustomNameTask
