import time
import asyncio
from threading import Thread


class IOThread(Thread):
    def __init__(self):
        super().__init__()
        self.loop = None

    def run(self):
        # create a new event loop and set it as default loop for this thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def start(self):
        # start thread and block until the event loop is ready
        super().start()
        while self.loop is None:
            time.sleep(0.01)

    def create_task(self, coro):
        future = asyncio.run_coroutine_threadsafe(coro, loop=self.loop)
        return asyncio.wrap_future(future)
