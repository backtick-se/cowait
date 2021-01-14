from .result import Result


class Node(object):
    """ Represents a node in a task DAG """
    __next_id = 1

    def __init__(self, task: str, inputs: dict = {}, id: int = None):
        self.id = Node.next_id() if id is None else id
        self.task = task
        self.inputs = inputs

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'Node{self.id}:{self.task}'

    def with_inputs(self, inputs):
        return Node(self.task, inputs, self.id)

    def output(self, accessor=None):
        if accessor is None:
            return Result(self, lambda output: output)
        return Result(self, accessor)

    @staticmethod
    def next_id() -> int:
        id = Node.__next_id
        Node.__next_id += 1
        return id
