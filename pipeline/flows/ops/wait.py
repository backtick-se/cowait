from typing import Any
from pipeline.tasks import TaskFuture, ReturnException
from .flow_op import FlowOp


class AwaitOp(FlowOp):
    def __init__(self, task: TaskFuture):
        super().__init__([ task ])
        self.task = task
        self._result = None

    def result(self) -> dict:
        return self._result

    def on_return(self, id: str, result: Any) -> None:
        if id == self.task.id:
            self._result = result
            raise ReturnException()


def Await(task: TaskFuture):
    # check if already complete
    if not task.waiting():
        return task.result

    # await completion
    return task.flow.op(AwaitOp(task))