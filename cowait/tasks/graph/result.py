

class Result(object):
    def __init__(self, node, accessor):
        self.node = node
        self.accessor = accessor

    def __repr__(self):
        return f'Result:N{self.node.id}:{self.accessor}'

    def get(self, outputs):
        if callable(self.accessor):
            return self.accessor(outputs)
        else:
            return outputs[self.accessor]
