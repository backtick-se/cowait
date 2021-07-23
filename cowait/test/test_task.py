import os
import pytest
import asyncio
from alt_pytest_asyncio.plugin import AltPytestAsyncioPlugin
from cowait import Task


class PytestTask(Task):
    async def run(
        self,
        marks=None,
        verbose: bool = True,
        capture: bool = True,
    ):
        plugins = [
            # make sure pytest uses the existing event loop
            AltPytestAsyncioPlugin(loop=asyncio.get_event_loop()),
        ]

        # use cowait's bundled pytest config if none is provided in the project root
        config = None
        if not os.path.exists('pytest.ini'):
            config = '/var/cowait/pytest.ini'

        args = create_pytest_args(
            config=config,
            verbose=verbose,
            marks=marks,
            capture=capture,
        )

        print('Args:', ' '.join(args))

        # run tests
        code = pytest.main(args, plugins=plugins)

        # throw an exception if the tests failed
        if code != pytest.ExitCode.OK and \
           code != pytest.ExitCode.NO_TESTS_COLLECTED:
            raise RuntimeError('Tests failed')

        return True


def create_pytest_args(config=None, marks=None, verbose=True, capture=True):
    args = []

    if config:
        args += ['-c', config]

    # verbose output
    if verbose:
        args.append('-vv')

    # output capture settings
    args.append('--capture=' + ('fd' if capture else 'no'))

    # marks
    if marks and len(marks) > 0:
        args += ["-m", marks]

    return args
