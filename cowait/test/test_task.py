import pytest
from cowait.tasks import Task
from cowait.test.fixtures import set_test_task


class PytestTask(Task):
    async def run(self, folder='context/'):
        set_test_task(self)
        pytest.main([folder])
