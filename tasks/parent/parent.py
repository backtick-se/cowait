from pipeline.flows import ConcurrentFlow, SequentialFlow


class LazyParentTask(ConcurrentFlow):
    def plan(self, durations, crash_at = -1, **inputs):
        Lazy = self.define(
            name='lazy',
            image='johanhenriksson/pipeline-task:lazy', 
            duration=10,
        )

        sleeps = [ ]
        for duration in durations:
            task = Lazy(duration=duration)
            sleeps.append(task)

        print('parent done')