import asyncio
from cowait.tasks import Task
from .graph import Graph


class GraphTask(Task):
    async def define(self, graph, **inputs):
        # override in subclasses
        pass

    async def run(self, **inputs):
        g = Graph()
        self.define(g, **inputs)

        # run until all nodes complete
        pending = []
        while not g.completed:
            # launch tasks for each node that is ready for execution
            while True:
                ready_node = g.next()
                if ready_node is None:
                    break

                # spawn task for node...
                ready_task = self.spawn(ready_node.task, inputs=ready_node.inputs)
                pending.append(ready_task)

            # if everything is completed, exit
            if len(pending) == 0:
                break

            # wait until any task finishes
            done, _ = asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            # mark finished nodes as completed
            for task in done:
                g.complete(task, task.result())
                pending.remove(task)

        # return what?
        return True
