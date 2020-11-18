import json


def option_val(val):
    try:
        return json.loads(val)
    except json.JSONDecodeError:
        return val


def option_dict(opts):
    options = {}
    for [key, val] in opts:
        options[key] = option_val(val)
    return options
