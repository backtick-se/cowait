from datetime import datetime
from marshmallow import Schema, fields, post_load
from pipeline.tasks.status import WAIT, WORK


class TaskList(object):
    def __init__(self):
        self.items = {}

    def __getitem__(self, key):
        return self.items[key]

    def __iter__(self):
        return self.items.values().__iter__()

    def task_ids(self):
        return self.items.keys()

    def attach(self, node):
        node.on('init', self.on_init)
        node.on('status', self.on_status)
        node.on('fail', self.on_fail)
        node.on('return', self.on_return)

    def detach(self, node):
        node.off('init', self.on_init)
        node.off('status', self.on_status)
        node.off('fail', self.on_fail)
        node.off('return', self.on_return)

    def on_init(self, task: dict):
        task = TaskListItem(**task)
        self.items[task.id] = task

    def on_status(self, id, status):
        if id not in self.items:
            return
        task = self.items[id]
        task.status = status
        if status == WORK:
            task.started_at = datetime.now()

    def on_fail(self, id, error):
        if id not in self.items:
            return
        task = self.items[id]
        task.error = error
        task.ended_at = datetime.now()

    def on_return(self, id, result):
        if id not in self.items:
            return
        task = self.items[id]
        task.result = result
        task.ended_at = datetime.now()


class TaskListItemSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    image = fields.Str()
    status = fields.Str(missing=WAIT)
    inputs = fields.Dict(missing={})
    meta = fields.Dict(missing={})
    env = fields.Dict(missing={})
    upstream = fields.Str(allow_none=True)
    created_at = fields.DateTime(allow_none=True)
    started_at = fields.DateTime(allow_none=True)
    ended_at = fields.DateTime(allow_none=True)
    result = fields.Raw(allow_none=True)
    error = fields.Str(allow_none=True)

    @post_load
    def make_task_item(self, data):
        return TaskListItem(**data)


schema = TaskListItemSchema()


class TaskListItem(object):
    def __init__(
        self,
        id,
        name,
        image,
        status=WAIT,
        upstream=None,
        env={},
        meta={},
        inputs={},
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.image = image
        self.status = status
        self.upstream = upstream
        self.inputs = inputs
        self.meta = meta
        self.env = env
        self.created_at = datetime.now()
        self.started_at = None
        self.ended_at = None
        self.result = None
        self.error = None

    def serialize(self):
        return schema.dump(self)

    def __str__(self):
        return schema.dumps(self)
