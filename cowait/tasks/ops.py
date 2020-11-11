import asyncio


async def join(tasks: list) -> list:
    """ Waits for a list of tasks to complete, returning a list containing their results. """
    return await asyncio.gather(*tasks)
