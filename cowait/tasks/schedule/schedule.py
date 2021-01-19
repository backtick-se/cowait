import traceback
from datetime import datetime
from cowait.tasks import Task, TaskError, rpc, sleep
from cowait.utils import parse_task_image_name
from .schedule_definition import ScheduleDefinition


def scheduled_task_id(name: str, date: datetime):
    name = name.replace('.', '-')
    name = name.replace('_', '-')
    name = name.lower()
    timestamp = date.strftime('%Y%m%d%H%M')
    return f'{name}-{timestamp}'


class ScheduleTask(Task):
    """
    ScheduleTask runs another task on a specified cron-style schedule.

    Inputs:
        schedule (str): Cron-style scheduling string, e.g. '0 8 * * *' for every day at 8am.
        target (str): Task to run.
        kwargs: All other inputs will be forwarded to the target task.

    Returns:
        Nothing. Runs forever.
    """

    async def run(self, schedule: str, target: str, **inputs):
        image, name = parse_task_image_name(target, default_image=self.image)

        # instantiate schedule
        self.schedule = ScheduleDefinition(schedule)

        print(f'Scheduled {name} ({image}) at {schedule}')
        print('The current time is', datetime.now())

        last_run = datetime(1970, 1, 1)
        while True:
            await sleep(1)

            now = datetime.now()
            if self.schedule.is_now():
                if self.schedule.is_at(last_run) \
                        and last_run.minute == now.minute:
                    continue

                last_run = now
                await self.execute(name, image, inputs)

    async def execute(self, name: str, image: str, inputs: dict):
        now = datetime.now()
        print('Execution triggered')

        try:
            result = await self.spawn(
                id=scheduled_task_id(name, now),
                name=name,
                image=image,
                inputs=inputs,
            )

            end = datetime.now()
            duration = end - now
            print(f'Finished in {duration}. Result:')
            print(result)

        except TaskError:
            end = datetime.now()
            duration = end - now
            print(f'Error after {duration}. Exception:')
            traceback.print_exc()

    @rpc
    async def reschedule(self, schedule):
        # instantiate/validate schedule
        self.schedule = ScheduleDefinition(schedule)
        return schedule
