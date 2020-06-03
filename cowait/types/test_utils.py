from .dict import Dict
from .simple import Any, Int
from .utils import get_return_type, get_parameter_types, get_parameter_defaults


def test_get_parameter_defaults():
    def test_func(a, b=1, c='hi'):
        pass

    defaults = get_parameter_defaults(test_func)
    assert 'a' not in defaults
    assert 'b' in defaults and defaults['b'] == 1
    assert 'c' in defaults and defaults['c'] == 'hi'


def test_get_parameter_types():
    def test_func(a, b: int, c: any):
        pass

    types = get_parameter_types(test_func)
    assert isinstance(types, Dict)

    shape = types.shape
    assert 'a' in shape and isinstance(shape['a'], Any)
    assert 'b' in shape and isinstance(shape['b'], Int)
    assert 'c' in shape and isinstance(shape['c'], Any)


def test_get_return_type():
    def returns_int() -> int:
        pass

    def returns_any():
        pass

    return_type = get_return_type(returns_int)
    assert isinstance(return_type, Int)

    return_type = get_return_type(returns_any)
    assert isinstance(return_type, Any)
