import pytest
from .types import InputType, is_input_type, convert_type, \
    String, Int, Float, Bool, Dict, List


class TestInputType(InputType):
    """ A custom input type """
    pass


class NotInputType(object):
    """ Another object that is not a valid type """
    pass


def test_is_input_type():
    assert is_input_type(str)
    assert is_input_type(int)
    assert is_input_type(float)
    assert is_input_type(bool)
    assert is_input_type(dict)
    assert is_input_type(list)
    assert is_input_type(TestInputType())
    assert not is_input_type(NotInputType)


def test_get_input_type():
    assert isinstance(convert_type(str), String)
    assert isinstance(convert_type(int), Int)
    assert isinstance(convert_type(float), Float)
    assert isinstance(convert_type(bool), Bool)
    assert isinstance(convert_type(dict), Dict)
    assert isinstance(convert_type(list), List)


def test_string():
    string = String()
    string.validate('hello', 'OK')
    string.validate(3, 'OK')
    string.validate(3.14, 'OK')

    assert string.deserialize(3) == '3'
    assert string.deserialize(3.14) == '3.14'
    assert string.deserialize('hello') == 'hello'


def test_integer():
    integer = Int()
    integer.validate(3, 'Three')
    integer.validate('6', 'Six')

    with pytest.raises(ValueError):
        integer.validate('shit', 'StringFail')

    with pytest.raises(ValueError):
        integer.validate('1.23', 'FloatFail')

    assert integer.deserialize(3) == 3
    assert integer.serialize(3) == 3


def test_float():
    float = Float()

    float.validate(3.14, 'Pi')
    float.validate('3.14', 'Pi')
    float.validate(3, 'Three')
    float.validate('3', 'Three')

    with pytest.raises(ValueError):
        float.validate('shit', 'StringFail')

    assert float.deserialize('3.14') == 3.14
    assert float.serialize(3.14) == 3.14


def test_bool():
    bool = Bool()

    bool.validate('True', 'True')
    bool.validate('false', 'False')

    with pytest.raises(ValueError):
        bool.validate(1, 'int')

    with pytest.raises(ValueError):
        bool.validate('', 'None')

    assert bool.deserialize('true')
    assert not bool.deserialize('false')
