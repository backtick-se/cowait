from cowait import Task


class Number(Task):
    # input values are received as keyword arguments to Task.run()
    async def run(self, first, second=2):
        print('Inputs:', first, second)

        return first
