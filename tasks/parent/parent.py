from pipeline.flows import ConcurrentFlow


class LazyParentTask(ConcurrentFlow):
    def plan(self, durations, crash_at = -1, **inputs):
        task = inputs.get('task', 'lazy')
        for duration in durations:
            self.spawn(
                name=task,
                duration=duration,
                crash_at=crash_at,
            )

        self.spawn(
            name=task,
            duration=2 * duration,
            crash_at=-1,
        )
