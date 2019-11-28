from io import StringIO
from unittest.mock import Mock
from .stream_capture import StreamCapture


def test_write():
    output = StringIO()
    cap = StreamCapture(output)

    cap.write('hello')
    assert cap.getvalue() == 'hello'
    assert cap.getvalue() == output.getvalue()


def test_newline_flush():
    cb = Mock()
    output = Mock()
    cap = StreamCapture(output, callback=cb)

    cap.write('hello ')
    assert cb.call_count == 0

    cap.write('team\n')
    assert cb.call_count == 1
    cb.assert_called_with('hello team\n')

    cap.write('again\n')
    assert cb.call_count == 2
    cb.assert_called_with('again\n')

    assert output.flush.call_count == 2
