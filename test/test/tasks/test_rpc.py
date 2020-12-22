from cowait.test import capture_task_events
from cowait.tasks import TASK_RETURN, TASK_STATUS, DONE


def test_rpc():
    # we expect to find two return values
    # and two success statuses
    output = capture_task_events('cowait.test.tasks.rpc_parent')
    assert output.count(type=TASK_RETURN) == 2
    assert output.count(type=TASK_STATUS, status=DONE) == 2
