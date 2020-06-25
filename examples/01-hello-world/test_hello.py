from hello import Hello


async def test_hello():
    result = await Hello()
    assert result is None
