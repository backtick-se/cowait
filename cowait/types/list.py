from .type import Type
from .simple import Any
from .mapping import is_cowait_type, convert_type, TypeAlias


@TypeAlias(list)
class List(Type):
    """ List type """

    def __init__(self, elementType: Type = Any()):
        if not is_cowait_type(elementType):
            raise ValueError('Element type is not a cowait Type')

        self.elementType = convert_type(elementType)

    def validate(self, value: list, name: str) -> None:
        if not isinstance(value, list):
            raise ValueError(f'{name} is not a list')

        for i, item in enumerate(value):
            self.elementType.validate(item, f'{name}[{i}]')

    def serialize(self, value: list) -> list:
        return [self.elementType.serialize(item) for item in value]

    def deserialize(self, value: list) -> list:
        return [self.elementType.deserialize(item) for item in value]
