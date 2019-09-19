from typing import Any
from pipeline.tasks import ReturnException
from .flow import Flow


class ConcurrentFlow(Flow):
    def init(self) -> None:
        self.results = { }


    def result(self) -> dict:
        return self.results


    def on_return(self, id: str, result: Any) -> None:
        if id in self.tasks:
            self.results[id] = result

        if len(self.results) == len(self.tasks):
            raise ReturnException()
