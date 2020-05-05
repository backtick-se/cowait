

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


class Dict(InputType):
    def __init__(self, shape: dict):
        for key, type in shape.items():
            if not isinstance(type, InputType):
                raise ValueError(f'Key {key} is not an InputType')

        self.shape = shape

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
    def __init__(self, elementType: InputType):
        self.elementType = elementType

    def validate(self, value, name):
        if not isinstance(value, list):
            raise ValueError(f'{name} is not a list')

        for i, item in enumerate(value):
            self.elementType.validate(item, f'{name}[{i}]')

    def serialize(self, value):
        return [self.elementType.serialize(item) for item in value]

    def deserialize(self, value):
        return [self.elementType.deserialize(item) for item in value]
