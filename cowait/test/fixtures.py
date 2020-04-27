import pytest
import nest_asyncio

__TEST_TASK = None


def set_test_task(task):
    global __TEST_TASK
    __TEST_TASK = task


@pytest.fixture(name='task_test')
def task_test():
    # apply asyncio patch
    nest_asyncio.apply()

    global __TEST_TASK
    return __TEST_TASK
