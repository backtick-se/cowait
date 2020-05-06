import inspect


def is_input_type(type):
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
        return isinstance(type, InputType)


def convert_type(annot):
    if annot == inspect._empty:
        return Mixed()
    elif annot == any:
        return Mixed()
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
    elif isinstance(annot, InputType):
        return annot
    else:
        raise TypeError('Expected an input type')


def get_return_type(task):
    sig = inspect.signature(task.run)
    return convert_type(sig.return_annotation)


def get_input_types(task):
    sig = inspect.signature(task.run)
    return Dict({
        key: convert_type(parameter.annotation)
        for key, parameter in sig.parameters.items()
        if parameter.kind == inspect._POSITIONAL_OR_KEYWORD
    })


class InputType(object):
    def validate(self, value, name):
        raise NotImplementedError()

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value


class Mixed(InputType):
    def validate(self, value, name):
        pass


class Int(InputType):
    def validate(self, value, name):
        try:
            int(value)
        except ValueError:
            raise ValueError(f'{name} must be an integer')

    def deserialize(self, value):
        return int(value)


class Float(InputType):
    def validate(self, value, name):
        try:
            float(value)
        except ValueError:
            raise ValueError(f'{name} must be a float')

    def deserialize(self, value):
        return float(value)


class String(InputType):
    def validate(self, value, name):
        try:
            str(value)
        except ValueError:
            raise ValueError(f'{name} must be a string')

    def deserialize(self, value):
        return str(value)


class Bool(InputType):
    def validate(self, value, name):
        if isinstance(value, bool):
            return True

        value = str(value).lower()
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            raise ValueError(f'{name} must be a boolean')

    def deserialize(self, value):
        if isinstance(value, bool):
            return value

        value = str(value).lower()
        if value == 'true':
            return True
        elif value == 'false':
            return False


class Dict(InputType):
    def __init__(self, shape: dict = {}):
        for key, type in shape.items():
            if not is_input_type(type):
                raise ValueError(f'Key {key} is not an InputType')

        self.shape = {key: convert_type(type) for key, type in shape.items()}

    def validate(self, value, name):
        if not isinstance(value, dict):
            raise ValueError(f'{name} is not a dictionary')

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


class List(InputType):
    def __init__(self, elementType: InputType = Mixed()):
        if not is_input_type(elementType):
            raise ValueError('Element type is not an InputType')

        self.elementType = convert_type(elementType)

    def validate(self, value, name):
        if not isinstance(value, list):
            raise ValueError(f'{name} is not a list')

        for i, item in enumerate(value):
            self.elementType.validate(item, f'{name}[{i}]')

    def serialize(self, value):
        return [self.elementType.serialize(item) for item in value]

    def deserialize(self, value):
        return [self.elementType.deserialize(item) for item in value]
