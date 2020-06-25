import pytest
from cowait.tasks.errors import TaskError
from typed_task import TypedTask


async def test_number():
    with pytest.raises(TaskError, match=r'.*ValueError.*'):
        await TypedTask(text='hi', number='string')

    result = await TypedTask()

    assert result == {
        'text': 'hi',
        'number': 5
    }
