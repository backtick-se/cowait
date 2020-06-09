from .type import Type
from .mapping import TypeAlias
from datetime import datetime


@TypeAlias(any)
class Any(Type):
    """ Any type. Disables typechecking. """

    name: str = 'any'

    def validate(self, value: any, name: str) -> None:
        pass


@TypeAlias(int)
class Int(Type):
    """ Integer, or anything that can be cast to an integer """

    name: str = 'int'

    def validate(self, value: int, name: str) -> None:
        try:
            int(value)
        except ValueError:
            raise ValueError(f'{name} must be an integer')

    def deserialize(self, value: any) -> int:
        return int(value)


@TypeAlias(float)
class Float(Type):
    """ Floating point, or anything that can be cast to a float """

    name: str = 'float'

    def validate(self, value: float, name: str) -> None:
        try:
            float(value)
        except ValueError:
            raise ValueError(f'{name} must be a float')

    def deserialize(self, value: any) -> float:
        return float(value)


@TypeAlias(str)
class String(Type):
    """ String """

    name: str = 'str'

    def validate(self, value: str, name: str) -> None:
        try:
            str(value)
        except ValueError:
            raise ValueError(f'{name} must be a string')

    def deserialize(self, value: any) -> str:
        return str(value)


@TypeAlias(bool)
class Bool(Type):
    """ Boolean """

    name: str = 'bool'

    def validate(self, value: bool, name: str) -> None:
        if isinstance(value, bool):
            return True

        value = str(value).lower()
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            raise ValueError(f'{name} must be a boolean')

    def deserialize(self, value: any) -> bool:
        if isinstance(value, bool):
            return value

        value = str(value).lower()
        if value == 'true':
            return True
        elif value == 'false':
            return False


@TypeAlias(datetime)
class DateTime(Type):
    """ Python datetime object serialized as an ISO8601 string """

    def validate(self, value: str, name: str) -> None:
        if isinstance(value, datetime):
            return

        if not isinstance(value, str):
            raise ValueError('Expected ISO8601 datetime')

        datetime.fromisoformat(value)

    def serialize(self, value: datetime) -> str:
        return value.isoformat()

    def deserialize(self, value: str) -> datetime:
        return datetime.fromisoformat(value)


@TypeAlias(None)
class Void(Type):
    def validate(self, value, name: str):
        if value is not None:
            raise ValueError(f'Expected {name} to be None')

    def serialize(self, value):
        return None

    def deserialize(self, value):
        return None
