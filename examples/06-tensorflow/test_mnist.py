from cowait.test import task_test
from mnist import MnistTask


@task_test
async def test_number(task_test):
  result = await task_test.spawn(MnistTask)

  assert result == 9
