import asyncio
from threading import Thread


class IOThread(Thread):
    def __init__(self):
        super().__init__()
        self.loop = None
        self._queue = []

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # schedule any queued tasks
        for coro in self._queue:
            self.create_task(coro)
        self._queue = []

        # run event loop
        self.loop.run_forever()

    def create_task(self, coro):
        # if the loop is not ready yet, queue it
        if self.loop is None:
            self._queue.append(coro)
            return

        future = asyncio.run_coroutine_threadsafe(coro, loop=self.loop)
        return asyncio.wrap_future(future)
