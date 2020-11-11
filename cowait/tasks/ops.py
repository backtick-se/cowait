import asyncio


async def join(tasks: list) -> list:
    """ Waits for a list of tasks to complete, returning a list containing their results. """
    return await asyncio.gather(*tasks)


async def wait(tasks: list, ignore_errors: bool = False) -> None:
    """ Waits for a list of tasks to complete. Returns nothing. """
    await asyncio.gather(*tasks, return_exceptions=ignore_errors)
