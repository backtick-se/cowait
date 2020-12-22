from .type import Type
from .simple import Any
from .mapping import is_cowait_type, convert_type, TypeAlias


@TypeAlias(list)
@TypeAlias(tuple)
class List(Type):
    """ List type """

    def __init__(self, item: Type = Any()):
        if not is_cowait_type(item):
            raise ValueError('Element type is not a cowait Type')

        self.item = convert_type(item)

    def validate(self, value: list, name: str) -> None:
        if not isinstance(value, list):
            raise ValueError(f'{name} is not a list')

        for i, item in enumerate(value):
            self.item.validate(item, f'{name}[{i}]')

    def serialize(self, value: list) -> list:
        return [self.item.serialize(item) for item in value]

    def deserialize(self, value: list) -> list:
        return [self.item.deserialize(item) for item in value]

    def describe(self):
        item_desc = self.item.describe()
        if item_desc is not None:
            return [item_desc]
        return []
