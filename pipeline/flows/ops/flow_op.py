from typing import Any
from pipeline.tasks import TaskError


class FlowOp(object):
    def __init__(self, tasks):
        self.tasks = { task.id: task for task in tasks }

    def handle(self, id: str, type: str, **msg) -> bool:
        if not id in self.tasks:
            return True

        if type == 'return':
            result = msg['result']
            self.tasks[id].done(result)
            self.on_return(id, result)

        elif type == 'fail':
            error = msg['error']
            self.tasks[id].fail(error)
            self.on_fail(id, error)

        return True


    def result(self) -> Any:
        """ Virtual method for creating a return value """
        return None


    def on_return(self, id: str, result: Any) -> None:
        """ Return message handler """
        pass


    def on_fail(self, id: str, error: str) -> None:
        """ Fail message handler """
        raise TaskError(error)