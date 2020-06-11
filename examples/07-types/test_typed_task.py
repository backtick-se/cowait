import pytest
from cowait.test import task_test
from cowait.tasks.errors import TaskError
from typed_task import TypedTask



@task_test
async def test_number(task_test):
  with pytest.raises(TaskError, match=r'.*ValueError.*'):
    await task_test.spawn(TypedTask, text='hi', number='string')

  result = await task_test.spawn(TypedTask)
  
  assert result == {
    'text': 'hi',
    'number': 5
  }
