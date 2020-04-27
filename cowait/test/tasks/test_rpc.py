from cowait.tasks import TaskDefinition
from cowait.engine.docker import DockerProvider
from cowait.utils.const import DEFAULT_BASE_IMAGE


def test_rpc():
    dp = DockerProvider()

    task = dp.spawn(TaskDefinition(
        name='cowait.test.tasks.rpc_parent',
        image=DEFAULT_BASE_IMAGE,
    ))

    # wait for execution
    result = task.container.wait()
    assert result['StatusCode'] == 0
