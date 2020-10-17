
class EventEmitter(object):
    def __init__(self):
        self.callbacks = {'*': []}

    def on(self, type: str, callback: callable) -> callable:
        try:
            self.callbacks[type].insert(0, callback)
        except KeyError:
            self.callbacks[type] = [callback]

        return callback

    def off(self, type: str, callback: callable) -> None:
        try:
            self.callbacks[type].remove(callback)
        except KeyError:
            pass

    async def emit(self, type: str, **kwargs: dict) -> None:
        if type == '*':
            raise ValueError('Cannot emit wildcard events')

        try:
            # wildcard events
            for callback in self.callbacks['*']:
                await callback(type=type, **kwargs)

            # actual event
            for callback in self.callbacks[type]:
                await callback(**kwargs)

        except KeyError:
            pass

    def emit_sync(self, type: str, **kwargs: dict) -> None:
        if type == '*':
            raise ValueError('Cannot emit wildcard events')

        try:
            # wildcard events
            for callback in self.callbacks['*']:
                callback(type=type, **kwargs)

            # actual event
            for callback in self.callbacks[type]:
                callback(**kwargs)

        except KeyError:
            pass
