from typing import Any
from pipeline.tasks import TaskError
from ..service import FlowService


class FlowOp(FlowService):
    def __init__(self, tasks):
        self.tasks = { task.id: task for task in tasks }


    def result(self) -> Any:
        """ Virtual method for creating a return value """
        return None


    def on_return(self, id: str, result: Any) -> None:
        """ Return message handler """
        if id in self.tasks:
            self.tasks[id].done(result)


    def on_fail(self, id: str, error: str) -> None:
        """ Fail message handler """
        if id in self.tasks:
            self.tasks[id].fail(error)
        raise TaskError(error)