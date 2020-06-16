from cowait.test import task_test
from number import Number


@task_test
async def test_number():
    input = 42
    result = await Number(first=input)

    assert result == input
