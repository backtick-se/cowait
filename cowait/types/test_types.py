import pytest
from .mapping import is_cowait_type, convert_type, get_type
from .simple import Any, String, Int, Float, Bool
from .dict import Dict
from .list import List


class TestType(Any):
    """ A custom input type """
    pass


class NotType(object):
    """ Another object that is not a valid type """
    pass


def test_is_cowait_type():
    assert is_cowait_type(str)
    assert is_cowait_type(int)
    assert is_cowait_type(float)
    assert is_cowait_type(bool)
    assert is_cowait_type(dict)
    assert is_cowait_type(list)
    assert is_cowait_type(TestType())
    assert not is_cowait_type(NotType)


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


def test_list():
    mixlist = List()
    mixlist.validate([1, 'str', 3.14], 'mix')

    # typed list
    intlist = List(Int())
    intlist.validate([1, 2], 'ok')

    with pytest.raises(ValueError):
        intlist.validate([1, 'woops'], 'fail')

    assert intlist.deserialize([1, 2]) == [1, 2]


def test_dict():
    dct = Dict({
        'text': String(),
        'number': Int(),
    })

    dct.validate({
        'text': 'hello',
        'number': 123,
    }, 'ok')

    # member missing
    with pytest.raises(ValueError):
        dct.validate({
            'text': 'hello',
        }, 'missing')

    # type error
    with pytest.raises(ValueError):
        dct.validate({
            'text': 'hello',
            'number': 'one'
        }, 'type err')


def test_composite():
    custom = Dict({
        'int_list': List(Int()),
        'subdict': Dict({
            'number': Int(),
        }),
    })

    custom.validate({
        'int_list': [1, 2],
        'subdict': {
            'number': 1,
        },
    }, 'ok')

    with pytest.raises(ValueError):
        custom.validate({
            'int_list': [1, 2],
            'subdict': {},
        }, 'subdict fail')


def test_instantiate_type():
    """ Ensures all default types can be auto instantiated """
    assert isinstance(convert_type(Any), Any)
    assert isinstance(convert_type(String), String)
    assert isinstance(convert_type(Int), Int)
    assert isinstance(convert_type(Float), Float)
    assert isinstance(convert_type(Bool), Bool)
    assert isinstance(convert_type(Dict), Dict)
    assert isinstance(convert_type(List), List)


def test_instantiate_with_non_default_params():
    class TypeWithParam(Any):
        def __init__(self, non_default):
            pass

    with pytest.raises(TypeError):
        convert_type(TypeWithParam)


def test_instantiate_with_default_params():
    class TypeWithParam(Any):
        def __init__(self, a=1):
            self.a = a

    obj = convert_type(TypeWithParam)
    assert isinstance(obj, TypeWithParam)
    assert obj.a == 1


def test_get_type():
    assert get_type('str') is String
    assert get_type('int') is Int
