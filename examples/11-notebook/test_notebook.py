import pytest
from cowait.tasks.notebook import NotebookRunner


@pytest.mark.async_timeout(700)
async def test_notebook():
    result1 = await NotebookRunner(path='simple.ipynb')
    seq1 = [a+1 for a in range(10)]
    assert result1 == {
        'sum': sum(seq1),
        'sq_sum': sum([a * a for a in seq1])
    }

    result2 = await NotebookRunner(path='simple.ipynb', N=5)
    seq2 = [a+1 for a in range(5)]
    assert result2 == {
        'sum': sum(seq2),
        'sq_sum': sum([a * a for a in seq2])
    }

    result3 = await NotebookRunner(path='simple.ipynb', N=0)
    assert result3 == 'failed'
