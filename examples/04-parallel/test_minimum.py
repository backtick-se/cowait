from cowait.test import task_test
from minimum import Minimum


@task_test
async def test_minimum():
    a = 43
    b = 42
    result = await Minimum(first=a, second=b)

    assert result == b
