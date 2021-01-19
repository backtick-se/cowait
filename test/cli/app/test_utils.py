import pytest
from cowait.cli.app.utils import parse_input, parse_input_list


def test_parse_parse_input():
    with pytest.raises(ValueError):
        parse_input('key')
    with pytest.raises(ValueError):
        parse_input('key=')
    with pytest.raises(ValueError):
        parse_input('=""')
    with pytest.raises(ValueError):
        parse_input('123=""')

    assert parse_input('key="="') == ('key', '=')
    assert parse_input('key=true') == ('key', True)
    assert parse_input('key=123') == ('key', 123)
    assert parse_input('dict={"hello":"world", "number":123}') == ('dict', {
        'hello': 'world',
        'number': 123,
    })
    assert parse_input('list=[1, 2, 3]') == ('list', [1, 2, 3])
    assert parse_input(' trim = " " ') == ('trim', ' ')
    assert parse_input('key=abc') == ('key', 'abc')


def test_parse_input_list():
    inputs = parse_input_list([
        'number=1',
        'text="string"',
        'flag=true',
    ])
    assert inputs == {
        'number': 1,
        'text': 'string',
        'flag': True,
    }

