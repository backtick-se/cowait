import traceback
from datetime import datetime
from pipeline.tasks import Task, sleep


class ScheduleTask(Task):
    async def run(self, schedule, target, **inputs):
        image = 'docker.backtick.se/task'
        name = target
        if '/' in target:
            s = target.rfind('/')
            image = target[:s]
            name = target[s+1:]
            if '/' not in image:
                # prepend default repo
                image = f'docker.backtick.se/{image}'

        # validate schedule
        is_schedule(schedule)

        print('Scheduled', image, name, 'at', schedule)

        last_run = datetime(1970, 1, 1)
        while True:
            await sleep(0.5)

            now = datetime.now()
            if is_schedule(schedule, now):
                if is_schedule(schedule, last_run) \
                        and last_run.minute == now.minute:
                    continue

                print(f'{now}: Time to run!')
                last_run = now
                result = await self.execute(name, image, inputs)
                print('finished.', result)

    async def execute(self, name, image, inputs):
        try:
            now = datetime.now()
            id = f'{name}-' + \
                 f'{now.year}{now.month:02d}{now.day:02d}' + \
                 f'{now.hour:02d}{now.minute:02d}'
            return await self.spawn(
                id=id,
                name=name,
                image=image,
                inputs=inputs,
                owner=self.owner,
                env=self.env,
                meta=self.meta,
            )
        except Exception:
            traceback.print_exc()


def is_schedule(schedule, time: datetime = None) -> bool:
    # m h D M DT
    # * * * * *

    parts = schedule.split(' ')
    if len(parts) != 5:
        raise RuntimeError('Invalid schedule syntax')

    minute, hour, date, month, dow = parts

    now = datetime.now() if time is None else time
    if not is_value(minute, now.minute):
        return False
    if not is_value(hour, now.hour):
        return False
    if not is_value(date, now.day):
        return False
    if not is_value(month, now.month):
        return False
    if not is_value(dow, now.weekday()):
        return False

    return True


def is_value(pattern: str, value: int) -> bool:
    if ',' in pattern:
        patterns = pattern.split(',')
        for pattern in patterns:
            if is_value(pattern, value):
                return True
        return False

    if pattern == '*':
        return True

    if '-' in pattern:
        dash = pattern.find('-')
        minimum = int(pattern[:dash])
        maximum = int(pattern[dash+1:])
        return value >= minimum and value <= maximum

    if '/' in pattern:
        slash = pattern.find('/')
        setting = pattern[:slash]
        divisor = int(pattern[slash+1:])
        if setting == '*':
            return value % divisor == 0
        else:
            raise RuntimeError("illegal divisor pattern")

    exact = int(pattern)
    return value == exact
