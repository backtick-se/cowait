from datetime import datetime


class ScheduleDefinition(object):
    def __init__(self, schedule):
        parts = schedule.split(' ')
        if len(parts) != 5:
            raise ValueError('Invalid schedule syntax')

        self.minute, self.hour, self.date, self.month, self.dow = parts

        # run a check to validate the schedule
        self.is_now()

    def is_now(self):
        return self.is_at(datetime.now())

    def is_at(self, time):
        if not schedule_match(self.minute, time.minute, 0, 59):
            return False
        if not schedule_match(self.hour, time.hour, 0, 23):
            return False
        if not schedule_match(self.date, time.day, 1, 31):
            return False
        if not schedule_match(self.month, time.month, 1, 12):
            return False
        if not schedule_match(self.dow, time.weekday(), 1, 7):
            return False
        return True


def schedule_match(pattern, value, min_val, max_val):
    def in_bounds(value):
        return value >= min_val and value <= max_val

    if pattern == '*':
        return True

    if ',' in pattern:
        patterns = pattern.split(',')
        for pattern in patterns:
            if schedule_match(pattern, value):
                return True
        return False

    if '-' in pattern:
        dash = pattern.find('-')
        minimum = int(pattern[:dash])
        if not in_bounds(minimum):
            raise ValueError(
                f'Range minimum {minimum} is out of range: '
                f'{min_val}-{max_val}')

        maximum = int(pattern[dash+1:])
        if not in_bounds(maximum):
            raise ValueError(
                f'Range maximum {maximum} is out of range: '
                f'{min_val}-{max_val}')

        return value >= minimum and value <= maximum

    if '/' in pattern:
        slash = pattern.find('/')
        setting = pattern[:slash]
        divisor = int(pattern[slash+1:])
        if setting == '*':
            return value % divisor == 0
        else:
            raise ValueError(
                "Illegal schedule divisor pattern. "
                "Only */n patterns are supported."
            )

    exact = int(pattern)
    if not in_bounds(exact):
        raise ValueError(
            f'Exact value {exact} is out of range: '
            f'{min_val}-{max_val}')

    return value == exact
