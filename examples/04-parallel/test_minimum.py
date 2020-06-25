from minimum import Minimum


async def test_minimum():
    a = 43
    b = 42
    result = await Minimum(first=a, second=b)

    assert result == b
