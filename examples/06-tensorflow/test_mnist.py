from cowait.test import task_test
from mnist import MnistTask


@task_test
async def test_number():
    result = await MnistTask()
    assert result == 9
