from maximum import Maximum


async def test_number():
    a = 43
    b = 42
    result = await Maximum(first=a, second=b)

    assert result == a
