from cowait.test import task_test
from fibonacci import Fibonacci


@task_test
async def test_fibonacci(task_test):
    result = await Fibonacci(n=3)
    assert result == 3
