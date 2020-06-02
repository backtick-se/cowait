from .dict import Dict
from .list import List
from .custom import CustomType
from .simple import Int, String
from .mapping import TypeAlias
from .utils import type_from_description


def test_deserialize_dict_type():
    desc = type_from_description({
        'text': 'str',
        'number': 'int',
    })
    assert isinstance(desc, Dict)
    assert isinstance(desc['text'], String)
    assert isinstance(desc['number'], Int)


def test_deserialize_list_type():
    desc = type_from_description(['str'])
    assert isinstance(desc, List)
    assert isinstance(desc.elementType, String)


class ComplexCustom(object):
    def __init__(self, text, number):
        self.text = text
        self.number = number


@TypeAlias(ComplexCustom)
class ComplexCustomType(CustomType):
    def __init__(self):
        super().__init__(ComplexCustom, {
            'text': String(),
            'number': Int(),
        })


def test_custom_type_serialization():
    obj = ComplexCustom(text='hej', number=3)
    type = ComplexCustomType()
    desc = type.describe()
    assert 'text' in desc and desc['text'] == String.name
    assert 'number' in desc and desc['number'] == Int.name

    data = type.serialize(obj)
    assert '@' in data and data['@'] == type.name
    assert 'text' in data and data['text'] == obj.text
    assert 'number' in data and data['number'] == obj.number

    obj2 = type.deserialize(data)
    assert obj2.text == obj.text
    assert obj2.number == obj.number
