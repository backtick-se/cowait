from typing import Any
from pipeline.tasks import ReturnException
from .flow_op import FlowOp


class JoinOp(FlowOp):
    def __init__(self, tasks: list):
        super().__init__(tasks)
        self.results = { }

    def result(self) -> dict:
        return self.results

    def on_return(self, id: str, result: Any) -> None:
        if id in self.tasks:
            self.results[id] = result

        if len(self.results) == len(self.tasks):
            raise ReturnException()


def Join(tasks: list):
    if len(tasks) == 0:
        return [ ]
    tasks = list(tasks)

    # check if already complete
    if all([ task.completed() for task in tasks ]):
        return [ task.result for task in tasks ]

    # await completion
    flow = tasks[0].flow
    return flow.op(JoinOp(tasks))