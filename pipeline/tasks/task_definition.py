from marshmallow import Schema, fields, post_load
from ..utils import uuid


class TaskDefinitionSchema(Schema):
    id        = fields.Str()
    name      = fields.Str()
    image     = fields.Str()
    env       = fields.Dict()
    config    = fields.Dict()
    inputs    = fields.Dict()
    namespace = fields.Str()
    parent    = fields.Str()

    @post_load
    def make_taskdef(self, data, **kwargs):
        return TaskDefinition(**data)


schema = TaskDefinitionSchema()


class TaskDefinition(object):
    def __init__(self, name, image, id = None, config = { }, inputs = { }, env = { }, namespace = 'default', parent='root'):
        self.id = '%s-%s' % (name, uuid()) if not id else id
        self.name = name
        self.image = image
        self.env = env
        self.config = config
        self.inputs = inputs
        self.namespace = namespace
        self.parent = parent


    def serialize(self) -> dict:
        return schema.dumps(self)


    @staticmethod
    def deserialize(taskdef: dict) -> TaskDefinition:
        return schema.loads(taskdef)


