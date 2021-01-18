import pytest
from mnist import MnistTask


@pytest.mark.async_timeout(300)
async def test_number():
    result = await MnistTask()
    assert result == 9
