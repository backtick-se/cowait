from __future__ import annotations
from .status import WAIT
from .definition import TaskDefinition


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
        taskdef = super().serialize()
        return {
            **taskdef,
            'status': self.status,
            'error': self.error,
            'result': self.result,
            'log': self.log,
        }

    @staticmethod
    def deserialize(instance: dict) -> TaskInstance:
        """ Deserialize task definition from a dict """
        taskdef = TaskDefinition.deserialize(instance).serialize()
        return TaskInstance(**{
            **taskdef,
            'status': instance.get('status', WAIT),
            'error': instance.get('error', None),
            'result': instance.get('result', None),
            'log': instance.get('log', None),
        })

