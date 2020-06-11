import pytest
from cowait import Task
from cowait.test.fixtures import CowaitFixturePlugin, set_test_task


class PytestTask(Task):
    async def run(self):
        set_test_task(self)
        code = pytest.main(plugins=[CowaitFixturePlugin()])
        if code != pytest.ExitCode.OK and \
           code != pytest.ExitCode.NO_TESTS_COLLECTED:
            raise RuntimeError('Tests failed')
