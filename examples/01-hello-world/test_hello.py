from cowait.test import task_test
from hello import Hello


@task_test
async def test_hello(task_test):
  result = await task_test.spawn(Hello)

  assert result == None
