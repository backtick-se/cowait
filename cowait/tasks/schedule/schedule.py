import traceback
from datetime import datetime
from cowait.tasks import Task, TaskError, rpc, sleep
from cowait.utils import parse_task_image_name
from .schedule_definition import ScheduleDefinition


class ScheduleTask(Task):
    async def run(self, schedule, target, **inputs):
        image, name = parse_task_image_name(target)

        # instantiate schedule
        self.schedule = ScheduleDefinition(schedule)

        print(f'Scheduled {name} ({image}) at {schedule}')
        print(f'The current time is', datetime.now())

        last_run = datetime(1970, 1, 1)
        while True:
            await sleep(0.5)

            now = datetime.now()
            if self.schedule.is_now():
                if self.schedule.is_at(last_run) \
                        and last_run.minute == now.minute:
                    continue

                last_run = now
                await self.execute(name, image, inputs)

    async def execute(self, name, image, inputs):
        now = datetime.now()
        print(f'{now} | Execution triggered')

        try:
            id = f'{name}-' + \
                 f'{now.year}{now.month:02d}{now.day:02d}' + \
                 f'{now.hour:02d}{now.minute:02d}'
            result = await self.spawn(
                id=id,
                name=name,
                image=image,
                inputs=inputs,
                owner=self.owner,
                env=self.env,
                meta=self.meta,
            )

            end = datetime.now()
            duration = end - now
            print(f'{end} | Finished in {duration}. Result:')
            print(result)

        except TaskError:
            end = datetime.now()
            duration = end - now
            print(f'{end} | Error after {duration}. Exception:')
            traceback.print_exc()

    @rpc
    async def reschedule(self, schedule):
        # instantiate/validate schedule
        self.schedule = ScheduleDefinition(schedule)
        return schedule
