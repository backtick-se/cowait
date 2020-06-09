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
    assert isinstance(desc.item, String)


class ComplexCustom(object):
    def __init__(self, text, number):
        self.text = text
        self.number = number


@TypeAlias(ComplexCustom)
class ComplexCustomType(CustomType):
    name = 'ComplexCustomType'

    def __init__(self):
        super().__init__(ComplexCustom, {
            'text': String(),
            'number': Int(),
        })


def test_custom_type_serialization():
    obj = ComplexCustom(text='hej', number=3)
    type = ComplexCustomType()

    desc = type.describe()
    assert desc == 'ComplexCustomType'

    data = type.serialize(obj)
    assert 'text' in data and data['text'] == obj.text
    assert 'number' in data and data['number'] == obj.number

    # the custom type should be available from the type registry
    # ensure deserialization yields a proper object with the expected values
    type2 = type_from_description(type.name)
    obj2 = type2.deserialize(data)
    assert isinstance(obj2, ComplexCustom)
    assert obj2.text == obj.text
    assert obj2.number == obj.number
