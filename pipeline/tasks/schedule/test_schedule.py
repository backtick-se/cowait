import pytest
from datetime import datetime
from .schedule import is_schedule, is_value


def test_is_value():
    assert is_value("*", 1)

    assert is_value("1", 1)
    assert not is_value("1", 2)

    assert is_value("0-2", 1)
    assert not is_value("0-2", 3)

    assert is_value("*/5", 5)
    assert not is_value("*/5", 6)


def test_is_schedule():
    assert is_schedule("* * * * *")

    # invalid format
    with pytest.raises(RuntimeError):
        is_schedule("* **")

    assert is_schedule("*/3 21 * * *", datetime(2000, 1, 1, 21, 3))
    assert not is_schedule("*/3 21 * * *", datetime(2000, 1, 1, 22, 3))
    assert not is_schedule("*/3 21 * * *", datetime(2000, 1, 1, 21, 4))

