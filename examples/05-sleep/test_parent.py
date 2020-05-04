from cowait.test import task_test
from parent import Parent


@task_test
async def test_parent(task_test):
    """
    This is an example of a black-box test of a task.
    Provided a set of input, assert what the output of a task will be.
    """

    result = await task_test.spawn(Parent, duration=1)
    assert result == [
        {
            'duration': 1,
        },
        {
            'duration': 1,
        },
    ]
