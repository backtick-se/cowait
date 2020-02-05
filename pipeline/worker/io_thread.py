import asyncio
from threading import Thread


class IOThread(Thread):
    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def create_task(self, coro):
        asyncio.run_coroutine_threadsafe(coro, loop=self.loop)
