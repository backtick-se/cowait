import pytest
from pipeline.tasks import Flow
from pipeline.test.fixtures import set_test_task


class TestTask(Flow):
    async def run(self):
        set_test_task(self)
        pytest.main([
            'context/',
        ])
