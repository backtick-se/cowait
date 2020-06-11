from cowait.test import task_test
from maximum import Maximum


@task_test
async def test_number(task_test):
  input1 = 43
  input2 = 42
  result = await task_test.spawn(Maximum, first=input1, second=input2)

  assert result == input1
