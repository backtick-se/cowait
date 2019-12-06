import asyncio


async def join(*tasks):
    return await asyncio.gather(*map(lambda t: t.result, tasks))
