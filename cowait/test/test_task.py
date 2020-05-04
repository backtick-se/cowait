import pytest
from cowait import Task
from cowait.test.fixtures import CowaitFixturePlugin, set_test_task


class PytestTask(Task):
    async def run(self):
        set_test_task(self)
        pytest.main(plugins=[CowaitFixturePlugin()])
