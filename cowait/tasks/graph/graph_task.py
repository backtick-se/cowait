import asyncio
from cowait.tasks import Task
from .graph import Graph


class GraphTask(Task):
    def init(self) -> dict:
        return {
            'ui': [
                {
                    'component': 'ui.cowait.io/task-graph',
                    'path': 'graph',
                },
            ]
        }

    async def define(self, graph, **inputs):
        # this is where you would define your graph nodes
        # to create a dag, override this function in a subclass
        pass

    async def run(self, **inputs):
        graph = Graph()
        await self.define(graph, **inputs)

        pending = []
        task_nodes = {}
        node_tasks = {}

        async def send_state():
            state = {}
            for node in graph.nodes:
                task = node_tasks.get(node, None)
                state[node.id] = {
                    'id': str(node.id),
                    'task': node.task if not issubclass(node.task, Task) else node.task.__module__,
                    'depends_on': [str(edge.id) for edge in node.edges],
                    'task_id': None if not task else task.id,
                }
            await self.set_state({'graph': state})

        await send_state()

        # run until all nodes complete
        while not graph.completed:
            # launch tasks for each node that is ready for execution
            while True:
                node = graph.next()
                if node is None:
                    break

                task = self.spawn(node.task, inputs=node.inputs)
                node_tasks[node] = task

                # wrap the task in a future and store it in a mapping from futures -> node
                # so we can find the node once the task completes
                task = asyncio.ensure_future(task)
                task_nodes[task] = node

                pending.append(task)

            await send_state()

            # if everything is completed, exit
            if len(pending) == 0:
                break

            # wait until any task finishes
            done, _ = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            # mark finished nodes as completed
            for task in done:
                node = task_nodes[task]

                try:
                    # unpacking the result will throw an exception if the task failed
                    graph.complete(node, task.result())
                except Exception as e:
                    graph.fail(node, e)

                pending.remove(task)

        if not graph.completed:
            raise Exception('Some tasks failed to finish')

        await send_state()

        # return what?
        return True
