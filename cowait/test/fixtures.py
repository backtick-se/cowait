import pytest
import nest_asyncio

TEST_TASK = None


def set_test_task(task):
    global TEST_TASK
    TEST_TASK = task


class CowaitFixturePlugin(object):
    @pytest.fixture(name='task_test')
    def task_test(self):
        # apply asyncio patch
        nest_asyncio.apply()
        print('task fixture')

        global TEST_TASK
        return TEST_TASK
