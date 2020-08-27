from __future__ import annotations
from marshmallow import fields, post_load
from .status import WAIT
from .definition import TaskDefinition, TaskDefinitionSchema


class TaskInstance(TaskDefinition):
    def __init__(
        self,
        status: str = WAIT,
        error: str = None,
        result: any = None,
        log: str = '',
        **data,
    ):
        super().__init__(**data)
        self.status = status
        self.error = error
        self.result = result
        self.log = log

    def serialize(self) -> dict:
        """ Serialize task definition to a dict """
        return TaskInstanceSchema().dump(self)

    @staticmethod
    def deserialize(instance: dict) -> TaskInstance:
        """ Deserialize task definition from a dict """
        return TaskInstanceSchema().load(instance)


class TaskInstanceSchema(TaskDefinitionSchema):
    status = fields.Str(missing=WAIT)
    error = fields.Str(allow_none=True)
    result = fields.Raw(allow_none=True)
    log = fields.Str(allow_none=True)

    def make_instance(self, data: dict) -> TaskInstance:
        return TaskInstance(**data)
