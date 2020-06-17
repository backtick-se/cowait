import json
import numpy as np
from .utils import serialize, deserialize


def test_serialize_np_int():
    i = np.int64(3)
    data = serialize(i)
    assert data == 3

    # should be possible to serialize
    json.dumps(data)

    i2 = deserialize(data, 'NumpyInt')
    assert isinstance(i2, np.int64)
    assert i2 == 3


def test_serialize_np_float():
    f = np.float64(3.14)
    data = serialize(f)
    assert data == 3.14

    # should be possible to serialize
    json.dumps(data)

    f2 = deserialize(data, 'NumpyFloat')
    assert isinstance(f2, np.float64)
    assert f2 == 3.14


def test_serialize_np_bool():
    b = np.bool_(True)
    data = serialize(b)
    assert data

    # should be possible to serialize
    json.dumps(data)

    b2 = deserialize(data, 'NumpyBool')
    assert isinstance(b2, np.bool_)
    assert b2


def test_serialize_np_array():
    arr = np.array([[1, 2], [1, 2]])
    data = serialize(arr)
    assert data == [[1, 2], [1, 2]]

    # should be possible to serialize
    json.dumps(data)

    arr2 = deserialize(data, 'NumpyArray')
    assert isinstance(arr2, np.ndarray)
    assert arr2.tolist() == [[1, 2], [1, 2]]


def test_serialize_nested_np():
    data = serialize({
        'num': np.int64(3),
    })
    assert type(data['num']) == int

    # should be possible to serialize
    json.dumps(data)
