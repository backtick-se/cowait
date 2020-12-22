from cowait.test import capture_task_events
from cowait.tasks import TASK_INIT, TASK_STATUS, TASK_FAIL, TASK_RETURN, WORK, DONE, FAIL


def test_task_success():
    """ Ensures that successful task executions emit all the basic events """
    output = capture_task_events('cowait.test.tasks.utility', inputs={'return': 'everything ok'})
    assert len(output.unique('id')) == 1
    assert output.has(type=TASK_INIT)
    assert output.has(type=TASK_STATUS, status=WORK)
    assert output.has(type=TASK_STATUS, status=DONE)
    assert output.has(type=TASK_RETURN, result='everything ok')
    assert not output.has(type=TASK_FAIL)
    assert not output.has(type=TASK_STATUS, status=FAIL)


def test_task_error():
    """ Ensures that failed task executions emit all the basic events """
    output = capture_task_events('cowait.test.tasks.utility', inputs={'error': True})
    assert len(output.unique('id')) == 1
    assert output.has(type=TASK_INIT)
    assert output.has(type=TASK_FAIL, error='test error')
    assert output.has(type=TASK_STATUS, status=FAIL)
    assert not output.has(type=TASK_RETURN)
    assert not output.has(type=TASK_STATUS, status=DONE)
