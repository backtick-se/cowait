import inspect
from abc import ABC, abstractmethod


def is_cowait_type(type):
    """ Checks if a type is a valid cowait type """
    if type == any:
        return True
    elif type == int:
        return True
    elif type == float:
        return True
    elif type == str:
        return True
    elif type == bool:
        return True
    elif type == dict:
        return True
    elif type == list:
        return True
    else:
        return isinstance(type, Type)


def convert_type_annotation(annot):
    """ Converts a type annotation to a cowait type """
    if annot == inspect._empty:
        return Any()
    elif annot == any:
        return Any()
    elif annot == int:
        return Int()
    elif annot == float:
        return Float()
    elif annot == str:
        return String()
    elif annot == bool:
        return Bool()
    elif annot == dict:
        return Dict()
    elif annot == list:
        return List()
    elif isinstance(annot, Type):
        return annot
    else:
        raise TypeError('Expected a valid cowait type')


def get_return_type(task):
    """ Gets the return type of a Task or task instance. """
    sig = inspect.signature(task.run)
    return convert_type_annotation(sig.return_annotation)


def get_input_types(task):
    """
    Gets the input types for a Task or task instance.
    Returns a Dict, mapping parameter names to cowait types.
    """
    sig = inspect.signature(task.run)
    return Dict({
        key: convert_type_annotation(parameter.annotation)
        for key, parameter in sig.parameters.items()
        if parameter.kind == inspect._POSITIONAL_OR_KEYWORD
    })


class Type(ABC):
    @abstractmethod
    def validate(self, value: any, name: str) -> None:
        raise NotImplementedError()

    def serialize(self, value: any) -> 'Type':
        return value

    def deserialize(self, value: any) -> 'Type':
        return value


class Any(Type):
    """ Any type. Disables typechecking. """
    def validate(self, value: any, name: str) -> None:
        pass


class Int(Type):
    """ Integer, or anything that can be cast to an integer """
    def validate(self, value: any, name: str) -> None:
        try:
            int(value)
        except ValueError:
            raise ValueError(f'{name} must be an integer')

    def deserialize(self, value: any) -> int:
        return int(value)


class Float(Type):
    """ Floating point, or anything that can be cast to a float """

    def validate(self, value: any, name: str) -> None:
        try:
            float(value)
        except ValueError:
            raise ValueError(f'{name} must be a float')

    def deserialize(self, value: any) -> float:
        return float(value)


class String(Type):
    """ String """

    def validate(self, value: any, name: str) -> None:
        try:
            str(value)
        except ValueError:
            raise ValueError(f'{name} must be a string')

    def deserialize(self, value: any) -> str:
        return str(value)


class Bool(Type):
    """ Boolean """

    def validate(self, value: any, name: str) -> None:
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


class Dict(Type):
    def __init__(self, shape: dict = {}):
        for key, type in shape.items():
            if not is_cowait_type(type):
                raise ValueError(f'Key {key} is not a cowait Type')

        self.shape = {
            key: convert_type_annotation(type)
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


class List(Type):
    def __init__(self, elementType: Type = Any()):
        if not is_cowait_type(elementType):
            raise ValueError('Element type is not a cowait Type')

        self.elementType = convert_type_annotation(elementType)

    def validate(self, value, name):
        if not isinstance(value, list):
            raise ValueError(f'{name} is not a list')

        for i, item in enumerate(value):
            self.elementType.validate(item, f'{name}[{i}]')

    def serialize(self, value):
        return [self.elementType.serialize(item) for item in value]

    def deserialize(self, value):
        return [self.elementType.deserialize(item) for item in value]
