import asyncio


async def join(tasks):
    return await asyncio.gather(*tasks)
    done, pending = await asyncio.wait(tasks)
    return list(done)


async def gather(*tasks):
    return await asyncio.gather(*tasks)
    done, pending = await asyncio.wait(tasks)
    return list(done)
