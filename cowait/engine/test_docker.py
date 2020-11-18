import json
import time
import pytest
import docker
import requests
from .docker import DockerProvider, LABEL_TASK_ID, LABEL_PARENT_ID
from cowait.tasks import TaskDefinition

TEST_IMAGE = 'cowait/task'
TEST_TASK = 'cowait.test.tasks.utility'


def test_create_docker_task():
    dp = DockerProvider()
    docker = dp.docker

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
    )

    # run task
    task = dp.spawn(taskdef)

    assert task.id == taskdef.id
    assert hasattr(task, 'container')
    assert hasattr(task.container, 'id')

    # try to grab the container from docker api
    container = docker.containers.get(task.container.id)
    assert task.container == container

    # make sure container is properly labeled
    assert container.labels[LABEL_TASK_ID] == task.id
    assert container.labels[LABEL_PARENT_ID] == 'parent'

    # test task will dump info as json, so we can pick it up
    # make sure it matches what we put in.
    task_dump = None
    for msg in task.logs():
        print(msg)
        if msg['type'] == 'task/log':
            task_dump = json.loads(msg['data'])

    # wait for container to execute
    result = container.wait()
    assert result['StatusCode'] == 0

    # taskdef
    assert task_dump is not None
    assert taskdef.serialize() == task_dump['taskdef']

    # actual environment variables
    for key, val in env_vars.items():
        assert task_dump['env'][key] == val


def test_kill_docker_task():
    dp = DockerProvider()

    task = dp.spawn(TaskDefinition(
        name=TEST_TASK,
        image=TEST_IMAGE,
        inputs={'forever': True},
    ))

    # ensure container exists
    dp.docker.containers.get(task.container.id)

    # destroy it
    dp.destroy(task.id)

    # ensure it no longer exists
    with pytest.raises(docker.errors.NotFound):
        try:
            dp.docker.containers.get(task.container.id)
        except requests.exceptions.ChunkedEncodingError:
            # workaround for docker for mac bug:
            # https://github.com/docker/docker-py/issues/2696
            raise docker.errors.NotFound('Not found')


def test_docker_child_task():
    dp = DockerProvider()

    task = dp.spawn(TaskDefinition(
        name=TEST_TASK,
        image=TEST_IMAGE,
        inputs={'child': True},
    ))

    # wait for the child to spawn
    child = None
    for i in range(0, 10):
        children = dp.find_child_containers(task.id)
        if len(children) > 0:
            child = children[0]
            break
        time.sleep(0.5)

    # make sure we got a child
    assert child is not None

    # test list tasks
    tasks = dp.list_all()
    assert task.id in tasks
    assert child.labels[LABEL_TASK_ID] in tasks

    # kill the whole family
    dp.destroy(task.id)

    children = dp.find_child_containers(task.id)
    assert len(children) == 0


def test_docker_task_error():
    dp = DockerProvider()

    task = dp.spawn(TaskDefinition(
        name=TEST_TASK,
        image=TEST_IMAGE,
        inputs={'error': True},
    ))

    container = dp.docker.containers.get(task.container.id)
    assert task.container == container

    result = container.wait()
    assert result['StatusCode'] != 0


def test_docker_child_error():
    dp = DockerProvider()

    task = dp.spawn(TaskDefinition(
        name=TEST_TASK,
        image=TEST_IMAGE,
        inputs={'child_error': True},
    ))

    container = dp.docker.containers.get(task.container.id)
    assert task.container == container

    # child error should cause the parent to fail
    result = container.wait()
    assert result['StatusCode'] != 0
