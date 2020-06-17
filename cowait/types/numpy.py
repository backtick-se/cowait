import numpy as np
from .type import Type
from .simple import Int, Float, Bool
from .mapping import TypeAlias


@TypeAlias(
    np.byte, np.ubyte, np.int8, np.uint8,
    np.short, np.ushort, np.int16, np.uint16,
    np.intc, np.uintc, np.int_, np.uint, np.int32, np.uint32,
    np.longlong, np.ulonglong, np.int64, np.uint64,
    np.intp, np.uintp,
)
class NumpyInt(Int):
    name = 'NumpyInt'

    def deserialize(self, value: int) -> np.int64:
        return np.int64(value)


@TypeAlias(
    np.half, np.float16,
    np.single, np.float32, np.float_,
    np.double, np.longdouble, np.float64,
)
class NumpyFloat(Float):
    name = 'NumpyFloat'

    def deserialize(self, value: float) -> np.float64:
        return np.float64(value)


@TypeAlias(np.bool_)
class NumpyBool(Bool):
    name = 'NumpyBool'

    def deserialize(self, value: bool) -> np.bool_:
        return np.bool_(value)


@TypeAlias(np.ndarray)
class NumpyArray(Type):
    name = 'NumpyArray'

    def validate(self, value: list, name: str) -> None:
        if not isinstance(value, list):
            raise ValueError(f'Expected {name} to be a list')

    def serialize(self, value: np.ndarray) -> list:
        return value.tolist()

    def deserialize(self, value: list) -> np.ndarray:
        return np.array(value)
