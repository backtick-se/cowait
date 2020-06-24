import json
import pytest
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
        '{"oh no this json',
        '":"is broken"}',
        '{"this one":"is not"}\n',
    ]
    with pytest.raises(json.JSONDecodeError):
        for _ in json_stream(parts):
            pass
