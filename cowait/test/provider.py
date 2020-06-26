from cowait.tasks import Task, TaskDefinition
from cowait.engine import DockerProvider
from cowait.utils.const import DEFAULT_BASE_IMAGE
from .event_log import EventLog


def get_test_provider():
    """ Returns an instance of the test cluster provider """
    # todo: pick provider based on env or something?
    # must be able to run all tests on different providers
    return DockerProvider()


def spawn_test_task(name, **taskdef: dict) -> Task:
    """ Spawns a task using the test cluster provider """
    provider = get_test_provider()
    return provider.spawn(TaskDefinition(**{
        'name': name,
        'image': DEFAULT_BASE_IMAGE,
        **taskdef
    }))


def capture_task_events(name, **taskdef: dict) -> EventLog:
    output = EventLog()
    task = spawn_test_task(name, **taskdef)
    output.collect(task.logs())
    return output
