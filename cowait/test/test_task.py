import pytest
import nest_asyncio
from cowait import Task


class PytestTask(Task):
    async def run(self):
        # apply a patch that allows nested asyncio loops
        nest_asyncio.apply()

        code = pytest.main()
        if code != pytest.ExitCode.OK and \
           code != pytest.ExitCode.NO_TESTS_COLLECTED:
            raise RuntimeError('Tests failed')
