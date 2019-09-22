
class TaskFuture(object):
    def __init__(self, flow, task):
        self.id = task.id
        self.flow = flow
        self.task = task
        self.error = None
        self.result = None

    def waiting(self) -> bool:
        return self.error is None and self.result is None

    def completed(self) -> bool:
        return not self.waiting()

    def done(self, result):
        self.result = result

    def fail(self, error: str):
        self.error = error

    def __str__(self) -> str:
        return self.task.__str__().replace('Task', 'TaskFuture', 1)