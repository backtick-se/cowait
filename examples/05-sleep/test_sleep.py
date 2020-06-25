from sleep import Sleep


async def test_sleep():
    """
    This is an example of a black-box test of a task.
    Provided a set of input, assert what the output of a task will be.
    """

    result = await Sleep(duration=1)
    assert result == {
        'duration': 1,
    }
