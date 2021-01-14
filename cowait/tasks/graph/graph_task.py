import asyncio
from cowait.tasks import Task
from .graph import Graph


class GraphTask(Task):
    async def define(self, graph, **inputs):
        # this is where you would define your graph nodes
        # to create a dag, override this function in a subclass
        pass

    async def run(self, **inputs):
        graph = Graph()
        await self.define(graph, **inputs)

        # run until all nodes complete
        pending = []
        node_tasks = {}
        while not graph.completed:
            # launch tasks for each node that is ready for execution
            while True:
                node = graph.next()
                if node is None:
                    break

                task = self.spawn(node.task, inputs=node.inputs)

                # wrap the task in a future and store it in a mapping from futures -> node
                # so we can find the node once the task completes
                task = asyncio.ensure_future(task)
                node_tasks[task] = node

                pending.append(task)

            # if everything is completed, exit
            if len(pending) == 0:
                break

            # wait until any task finishes
            done, _ = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            # mark finished nodes as completed
            for task in done:
                node = node_tasks[task]

                try:
                    # unpacking the result will throw an exception if the task failed
                    graph.complete(node, task.result())
                except Exception as e:
                    graph.fail(node, e)

                pending.remove(task)

        if not graph.completed:
            raise Exception('Some tasks failed to finish')

        # return what?
        return True
