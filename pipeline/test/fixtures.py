import pytest
import nest_asyncio

__TEST_TASK = None


def set_test_task(task):
    global __TEST_TASK
    __TEST_TASK = task


@pytest.fixture
def tester():
    # ensure nested asyncio is supported
    nest_asyncio.apply()

    global __TEST_TASK
    return __TEST_TASK
