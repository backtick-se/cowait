from cowait import Task


class Hello(Task):
    async def run(self):
        print('Hello World')
