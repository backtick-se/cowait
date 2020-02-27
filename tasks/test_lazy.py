import pytest
from pipeline.test import tester
from lazy import Lazy


@pytest.mark.asyncio
async def test_lazy(tester):
    result = await tester.task(Lazy, duration=1)
    assert result == {
        'duration': 1,
        'crash_at': -1,
    }
