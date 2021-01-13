

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

    @staticmethod
    def wrap_input(input) -> 'Result':
        if isinstance(input, Node):
            return Result(input, lambda x: x)
        return input


class Graph(object):
    def __init__(self):
        self.nodes = []
        self.todo = []
        self.results = {}
        self.errors = {}

    @property
    def completed(self):
        return len(self.todo) == 0

    def node(self, task: str, inputs: dict = {}):
        node = Node(task, {
            key: Result.wrap_input(input)
            for key, input in inputs.items()
        })
        self.nodes.append(node)
        self.todo.append(node)
        return node

    def has_missing_input(self, node: Node) -> bool:
        for _, input in node.inputs.items():
            if input.node not in self.results:
                return True
        return False

    def has_upstream_failure(self, node: Node) -> bool:
        for _, input in node.inputs.items():
            if input.node in self.errors:
                return True
        return False

    def next(self) -> Node:
        idx = 0
        while idx < len(self.todo):
            node = self.todo[idx]

            # check for upstream failures
            if self.has_upstream_failure(node):
                self.fail(node, Exception('Upstream dependency failure'))
                continue

            # increment index after the failure check, since calling self.fail()
            # will remove a node from the list.
            idx += 1

            # check if the node is ready for execution
            if self.has_missing_input(node):
                continue

            # collect input values
            args = {}
            for key, input in node.inputs.items():
                if isinstance(input, Result):
                    outputs = self.results[input.node]
                    args[key] = input.get(outputs)
                else:
                    args[key] = input

            self.todo.remove(node)
            return node.with_inputs(args)

        return None

    def reset(self):
        self.todo = self.nodes.copy()
        self.errors = {}
        self.results = {}

    def complete(self, node, result):
        if node in self.errors:
            raise Exception('Node already failed')
        if node in self.todo:
            self.todo.remove(node)
        self.results[node] = result

    def fail(self, node, exception):
        if node in self.errors:
            raise Exception('Node already completed')
        if node in self.todo:
            self.todo.remove(node)
        self.errors[node] = exception
