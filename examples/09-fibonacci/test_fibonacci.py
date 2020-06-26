import pytest
from fibonacci import Fibonacci


@pytest.mark.async_timeout(30)
async def test_fibonacci():
    result = await Fibonacci(n=3)
    assert result == 3
