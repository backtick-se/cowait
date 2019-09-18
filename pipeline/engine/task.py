from abc import ABC, abstractmethod
from ..utils import uuid

class TaskDefinition(object):
    def __init__(self, name, image, config = { }, inputs = { }, env = { }, namespace = 'default'):
        self.id = '%s-%s' % (name, uuid())
        self.name = name
        self.image = image
        self.env = env
        self.config = config
        self.inputs = inputs
        self.namespace = namespace

    def serialize(self):
        return {
            'id':     self.id,
            'config': self.config,
            'inputs': self.inputs,
        }



class TaskContext(object):
    def __init__(self, cluster, config = { }):
        self.cluster = cluster
        self.config = config



class Task(ABC):
    def __init__(self, cluster, taskdef):
        self.cluster = cluster
        self.taskdef = taskdef
        super().__init__()


    def wait(self):
        self.cluster.wait(self)


    def logs(self):
        return self.cluster.wait(self)