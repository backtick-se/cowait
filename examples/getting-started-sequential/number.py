from cowait import Task


class Number(Task):
    async def run(self, value):
        return value
