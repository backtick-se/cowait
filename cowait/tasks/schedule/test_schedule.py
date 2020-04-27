import pytest
from datetime import datetime
from .schedule_definition import ScheduleDefinition, schedule_match


def test_is_value():
    assert schedule_match("*", 1, 0, 100)

    assert schedule_match("1", 1, 0, 100)
    assert not schedule_match("1", 2, 0, 100)

    assert schedule_match("0-2", 1, 0, 100)
    assert not schedule_match("0-2", 3, 0, 100)

    assert schedule_match("*/5", 5, 0, 100)
    assert not schedule_match("*/5", 6, 0, 100)

    with pytest.raises(ValueError):
        schedule_match("61 * * * *", 1, 0, 59)

    with pytest.raises(ValueError):
        schedule_match("1 * * * *", 1, 10, 59)


def test_is_schedule():
    def is_schedule(schedule, time):
        s = ScheduleDefinition(schedule)
        return s.is_at(time)

    assert is_schedule("* * * * *", datetime.now())

    # invalid format
    with pytest.raises(ValueError):
        is_schedule("* **", datetime.now())

    assert is_schedule("*/3 21 * * *", datetime(2000, 1, 1, 21, 3))
    assert not is_schedule("*/3 21 * * *", datetime(2000, 1, 1, 22, 3))
    assert not is_schedule("*/3 21 * * *", datetime(2000, 1, 1, 21, 4))
