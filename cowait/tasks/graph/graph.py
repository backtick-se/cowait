

class Node(object):
    """ Represents a node in a task DAG """

    def __init__(self, task: str, inputs: dict = {}):
        self.task = task
        self.inputs = inputs

    def with_inputs(self, inputs):
        return Node(self.task, inputs)

    def output(self, accessor):
        return Result(self, accessor)


class Result(object):
    def __init__(self, node, accessor):
        self.node = node
        self.accessor = accessor

    def get(self, outputs):
        if callable(self.accessor):
            return self.accessor(outputs)
        else:
            return outputs[self.accessor]


class Graph(object):
    def __init__(self):
        self.nodes = []
        self.todo = []
        self.ready = {}

    @property
    def completed(self):
        return len(self.todo) == 0

    def node(self, task: str, inputs: dict = {}):
        node = Node(task, inputs)
        self.nodes.append(node)
        self.todo.append(node)
        return node

    def next(self) -> Node:
        for node in self.todo:
            args = {}
            ready = True
            for key, input in node.inputs.items():
                if isinstance(input, Node):
                    # the input is a node - check if its output is available
                    if input not in self.ready:
                        ready = False
                        break
                    args[key] = self.ready[input]

                elif isinstance(input, Result):
                    if input.node not in self.ready:
                        ready = False
                        break

                    outputs = self.ready[input.node]
                    args[key] = input.get(outputs)

                else:
                    args[key] = input

            # ensure all inputs are ready, otherwise consider another task
            if not ready:
                continue

            self.todo.remove(node)
            return node.with_inputs(args)

        return None

    def reset(self):
        self.todo = self.nodes.copy()

    def complete(self, node, result):
        if node in self.todo:
            self.todo.remove(node)
        self.ready[node] = result
