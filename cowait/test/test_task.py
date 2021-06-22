import pytest
import asyncio
from alt_pytest_asyncio.plugin import AltPytestAsyncioPlugin
from cowait import Task


class PytestTask(Task):
    async def run(self, marks=None):
        plugins = [
            # make sure pytest uses the existing event loop
            AltPytestAsyncioPlugin(loop=asyncio.get_event_loop()),
        ]

        args = [
            # use cowait's bundled pytest settings
            "-c", "/var/cowait/pytest.ini",
        ]

        # add pytest marks to args
        if marks and len(marks) > 0:
            print('Marks:', marks)
            args += ["-m", marks]

        # run tests
        code = pytest.main(args, plugins=plugins)

        # throw an exception if the tests failed
        if code != pytest.ExitCode.OK and \
           code != pytest.ExitCode.NO_TESTS_COLLECTED:
            raise RuntimeError('Tests failed')
