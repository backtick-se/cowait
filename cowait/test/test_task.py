import pytest
import asyncio
from alt_pytest_asyncio.plugin import AltPytestAsyncioPlugin
from cowait import Task


class PytestTask(Task):
    async def run(self):
        loop = asyncio.get_event_loop()

        plugins = [
            AltPytestAsyncioPlugin(loop=loop),
        ]

        code = pytest.main(["-c", "/var/cowait/pytest.ini"], plugins=plugins)
        if code != pytest.ExitCode.OK and \
           code != pytest.ExitCode.NO_TESTS_COLLECTED:
            raise RuntimeError('Tests failed')
