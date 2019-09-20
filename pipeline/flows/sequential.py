from typing import Any
from pipeline.tasks import Task
from .flow import Flow
from .ops import Await, Join


class SequentialFlow(Flow):
    """ Runs all defined tasks in sequence. """

    def task(self, **taskdef) -> Task:
        task = super().task(**taskdef)
        # immediately awaiting the task causes a sequential flow:
        return Await(task)


    def run(self, **inputs) -> Any:
        super().run(**inputs)
        # we can still use a join to gather the results:
        return Join(self.tasks.values())
