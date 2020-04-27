import asyncio


async def join(*tasks):
    return await asyncio.gather(*tasks)
    done, pending = await asyncio.wait(tasks)
    return list(done)
