from .type import Type
from .simple import Any
from .mapping import is_cowait_type, convert_type, TypeAlias


@TypeAlias(dict)
class Dict(Type):
    """ Dictionary type """

    def __init__(self, shape: dict = {}):
        for key, type in shape.items():
            if not is_cowait_type(type):
                raise ValueError(f'Key {key} is not a cowait Type')

        self.shape = {
            key: convert_type(type)
            for key, type in shape.items()
        }

    def validate(self, value: dict, name: str) -> None:
        if not isinstance(value, dict):
            raise ValueError(f'{name} is not a dict')

        for key, type in self.shape.items():
            if key not in value:
                raise ValueError(f'{name}[{key}] is required')
            type.validate(value[key], f'{name}[{key}]')

    def serialize(self, value: dict) -> dict:
        any = Any()
        return {
            key: self.shape.get(key, any).serialize(value)
            for key, value in value.items()
        }

    def deserialize(self, value: dict) -> dict:
        any = Any()
        return {
            key: self.shape.get(key, any).deserialize(value)
            for key, value in value.items()
        }

    def describe(self):
        desc = {}
        for key, type in self.shape.items():
            type_desc = type.describe()
            if type_desc is not None:
                desc[key] = type_desc
        return desc

    def __getitem__(self, key):
        return self.shape[key]
