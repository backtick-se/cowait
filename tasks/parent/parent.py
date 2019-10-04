from pipeline.flows import Flow


class LazyParentTask(Flow):
    async def plan(self, duration, crash_at = -1, **inputs):
        print('first sleep:')
        await self.task(
            name='lazy',
            image='johanhenriksson/pipeline-task:lazy', 
            duration=duration,
            crash_at=-1,
        )

        print('second sleep:')
        await self.task(
            name='lazy',
            image='johanhenriksson/pipeline-task:lazy', 
            duration=duration,
            crash_at=-1,
        )
