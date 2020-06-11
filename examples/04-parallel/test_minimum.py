from cowait.test import task_test
from minimum import Minimum


@task_test
async def test_minimum(task_test):
  input1 = 43
  input2 = 42
  result = await task_test.spawn(Minimum, first=input1, second=input2)

  assert result == input2
