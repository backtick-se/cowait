from pipeline.flows import ConcurrentFlow


class LazyParentTask(ConcurrentFlow):
    def plan(self, durations, crash_at = -1, **inputs):
        task = inputs.get('task', 'lazy')
        image = f'johanhenriksson/pipeline-task:{task}'
        for duration in durations:
            self.spawn(
                name=task,
                image=image,
                inputs={
                    'duration': duration,
                    'crash_at': crash_at,
                },
            )

        self.spawn(
            name=task,
            image=image,
            inputs={
                'duration': 2 * duration,
                'crash_at': -1,
            },
        )
