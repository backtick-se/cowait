from cowait.test import task_test
from hello import Hello


@task_test
async def test_hello():
    result = await Hello()
    assert result is None
