import pytest
from pipeline.tasks import Task
from pipeline.test.fixtures import set_test_task


class PytestTask(Task):
    async def run(self):
        set_test_task(self)
        pytest.main([
            'context/',
        ])
