from number import Number


async def test_number():
    input = 42
    result = await Number(first=input)

    assert result == input
