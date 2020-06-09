import json
from cowait.tasks import TaskDefinition
from .kubernetes import KubernetesProvider
from .const import LABEL_TASK_ID, LABEL_PARENT_ID

TEST_IMAGE = 'cowait/task'
TEST_TASK = 'cowait.test.tasks.utility_task'


def test_create_kube_task():
    kp = KubernetesProvider()

    env_vars = {'hello': 'team'}

    taskdef = TaskDefinition(
        name=TEST_TASK,
        image=TEST_IMAGE,
        parent='parent',
        env=env_vars,
        inputs={
            'hello': '123',
            'child': False,
        },

        # disables any output.
        # this is hacky and should be refactored
        # we need a proper way to disable all logging
        upstream='disabled',
    )

    # run task
    task = kp.spawn(taskdef)

    assert task.id == taskdef.id
    assert hasattr(task, 'container')
    assert hasattr(task.container, 'id')

    # try to find pod
    pod = kp.wait_until_ready(task.id, timeout=10)

    # make sure pod is properly labeled
    assert pod.meta.labels == {
        LABEL_TASK_ID: task.id,
        LABEL_PARENT_ID: 'parent',
    }

    # test task will dump info as json, so we can pick it up
    # make sure it matches what we put in.
    logs = kp.logs(task)
    task_dump = json.loads(logs)

    # taskdef
    assert taskdef.serialize() == task_dump['taskdef']

    # actual environment variables
    for key, val in env_vars.items():
        assert task_dump['env'][key] == val
