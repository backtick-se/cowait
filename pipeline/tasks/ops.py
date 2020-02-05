import asyncio


async def join(*tasks):
    return await asyncio.gather(
        *map(lambda t: asyncio.wrap_future(t.result), tasks)
    )
