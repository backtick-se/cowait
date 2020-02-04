
class EventEmitter(object):
    def __init__(self):
        self.callbacks = {'*': []}

    def on(self, type: str, callback: callable) -> None:
        try:
            self.callbacks[type].append(callback)
        except KeyError:
            self.callbacks[type] = [callback]

    def off(self, type: str, callback: callable) -> None:
        try:
            self.callbacks[type].remove(callback)
        except KeyError:
            pass

    async def emit(self, type: str, **kwargs: dict) -> None:
        if type == '*':
            raise RuntimeError('Cannot emit wildcard events')

        try:
            # wildcard events
            for callback in self.callbacks['*']:
                await callback(type=type, **kwargs)

            # actual event
            for callback in self.callbacks[type]:
                await callback(**kwargs)

        except KeyError:
            pass