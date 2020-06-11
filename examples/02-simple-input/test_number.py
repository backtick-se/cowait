from cowait.test import task_test
from number import Number


@task_test
async def test_number(task_test):
  input = 42
  result = await task_test.spawn(Number, first=input)

  assert result == input
