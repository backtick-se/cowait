from abc import ABC, abstractmethod


class Task(ABC):
    def __init__(self, context):
        self.id       = context.id
        self.cluster  = context.cluster
        self.upstream = context.upstream
        self.inputs   = context.inputs
        self.parent   = context.parent


    def run(self, **inputs):
        pass


    def stop(self):
        pass


    def wait(self):
        self.cluster.wait(self)


    def logs(self):
        return self.cluster.logs(self)