from parent import Parent


async def test_parent():
    """
    This is an example of a black-box test of a task.
    Provided a set of input, assert what the output of a task will be.
    """

    result = await Parent(duration=1)
    assert result == [
        {
            'duration': 1,
        },
        {
            'duration': 1,
        },
    ]
