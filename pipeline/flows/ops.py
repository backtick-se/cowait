import asyncio


async def join(*tasks):
    return await asyncio.gather(*tasks)


async def map(tasks: list, transform: callable):
    results = await join(tasks)
    return [await transform(r) for r in results]
