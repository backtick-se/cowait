from pipeline.tasks import TaskDefinition
from pipeline.engine.docker import DockerProvider
from pipeline.utils.const import DEFAULT_BASE_IMAGE


def test_rpc():
    dp = DockerProvider()

    task = dp.spawn(TaskDefinition(
        name='pipeline.test.tasks.rpc_parent',
        image=DEFAULT_BASE_IMAGE,
    ))

    # wait for execution
    result = task.container.wait()
    assert result['StatusCode'] == 0
