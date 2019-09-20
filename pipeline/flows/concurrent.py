from typing import Any
from .flow import Flow
from .ops import Join


class ConcurrentFlow(Flow):
    """ Runs all defined tasks in parallell """

    def run(self, **inputs) -> Any:
        super().run(**inputs)
        return Join(self.tasks.values())
