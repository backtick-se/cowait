from pipeline.flows import ConcurrentFlow


class LazyParentTask(ConcurrentFlow):
    def plan(self, duration, crash_at = -1, **inputs):
        Lazy = self.define(
            name='lazy',
            image='johanhenriksson/pipeline-task:lazy', 
            duration=duration,
            crash_at=-1,
        )

        lazy1 = Lazy()
        lazy2 = Lazy(crash_at=crash_at)
