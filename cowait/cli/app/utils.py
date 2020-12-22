import json
import re

identifier = re.compile(r"^[^\d\W]\w*\Z", re.UNICODE)


def parse_input(value: str) -> tuple:
    if '=' not in value:
        raise ValueError('Input is not on key=value format')

    split = value.index('=')
    key = value[:split].strip()
    value = value[split+1:].strip()

    if identifier.match(key) is None:
        raise ValueError('Input key must be a valid identifier')

    try:
        value = json.loads(value)
    except json.JSONDecodeError:
        raise ValueError('Input value is not valid JSON')

    return key, value


def parse_input_list(inputs: list) -> dict:
    output = {}
    for input in inputs:
        key, value = parse_input(input)
        output[key] = value
    return output

