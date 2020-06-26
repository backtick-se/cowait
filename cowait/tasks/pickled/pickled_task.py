import inspect
from ..task import Task
from .pickle_task import unpickle_task


class PickledTask(Task):
    async def run(self, func: str, **inputs):
        func = unpickle_task(func)
        if inspect.iscoroutinefunction(func):
            return await func(**inputs)
        else:
            return func(**inputs)
