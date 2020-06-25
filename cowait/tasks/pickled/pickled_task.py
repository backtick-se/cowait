import dill
import base64
from cowait import Task


class PickledTask(Task):
    async def run(self, func: str, **inputs):
        funcbytes = base64.b64decode(func)
        func = dill.loads(funcbytes)
        return await func(**inputs)
