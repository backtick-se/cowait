from .json_stream import json_stream


def test_json_stream():
    parts = [
        '{"oh no this json',
        '":"is broken"}\n',
        '{"this one":"is not"}\n',
        'and this wont be processed',
    ]
    chunks = [c for c in json_stream(parts)]
    assert len(chunks) == 2


def test_json_stream_fail():
    parts = [
        '{"oh no this json', '":"is broken"}\n',
        'wtf is this?\n'
        '{"this one":"is not"}\n',
    ]
    for msg in json_stream(parts):
        if 'type' in msg and msg['type'] == 'core/error':
            return
    assert False


def test_json_stream_empty():
    parts = [' \n', '  ', '\n']
    assert len([p for p in json_stream(parts)]) == 0
