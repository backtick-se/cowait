import pytest
from imdb import ImdbTask


@pytest.mark.async_timeout(700)
async def test_number():
    result = await ImdbTask()
    assert result == 1
    