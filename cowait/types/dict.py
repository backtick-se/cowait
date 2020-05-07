from .type import Type
from .utils import is_cowait_type, convert_type


class Dict(Type):
    def __init__(self, shape: dict = {}):
        for key, type in shape.items():
            if not is_cowait_type(type):
                raise ValueError(f'Key {key} is not a cowait Type')

        self.shape = {
            key: convert_type(type)
            for key, type in shape.items()
        }

    def validate(self, value: dict, name: str):
        if not isinstance(value, dict):
            raise ValueError(f'{name} is not a dict')

        for key, type in self.shape.items():
            if key not in value:
                raise ValueError(f'{name}[{key}] is required')
            type.validate(value[key], f'{name}[{key}]')

    def serialize(self, value):
        return {
            key: type.serialize(value[key])
            for key, type in self.shape.items()
        }

    def deserialize(self, value):
        return {
            key: type.deserialize(value[key])
            for key, type in self.shape.items()
        }
