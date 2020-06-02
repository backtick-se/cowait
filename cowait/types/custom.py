from .type import Type


class CustomType(Type):
    def __init__(self, cls, shape: dict):
        self.cls = cls
        self.shape = shape

    def validate(self, value):
        if not isinstance(value, dict):
            raise TypeError('Expected a dict')
        for key, type in self.shape.items():
            type.validate(value[key])

    def serialize(self, value):
        return {
            key: type.serialize(getattr(value, key))
            for key, type in self.shape.items()
        }

    def deserialize(self, value):
        return self.cls(**{
            key: type.deserialize(value[key])
            for key, type in self.shape.items()
        })
