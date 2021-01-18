

class UIComponent(object):
    def __init__(self, task, id: str, component: str):
        self.id = id
        self.task = task
        self.component = component
        self.state = {}

    async def set_state(self, state: dict) -> None:
        self.state = {
            **self.state,
            **state,
        }
        await self.task.set_state({self.id: self.state})

    def __getattr__(self, key):
        return self.get(key)

    def get(self, key):
        if key not in self.state:
            raise AttributeError(f'No such state variable {key}')
        return self.state[key]

    async def set(self, key, value):
        if key not in self.state:
            raise AttributeError(f'No such state variable {key}')
        await self.set_state({key: value})

    def to_json(self):
        return {
            'id': self.id,
            'component': self.component,
        }
