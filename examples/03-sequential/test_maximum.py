from cowait.test import task_test
from maximum import Maximum


@task_test
async def test_number():
    a = 43
    b = 42
    result = await Maximum(first=a, second=b)

    assert result == a
