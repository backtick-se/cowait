from __future__ import annotations
from datetime import datetime, timezone
from marshmallow import Schema, fields, post_load
from ..utils import uuid


def generate_task_id(name: str) -> str:
    if '.' in name:
        dot = name.rfind('.')
        name = name[dot+1:]

    name = name.replace('.', '-')
    name = name.replace('_', '-')

    return '%s-%s' % (name.lower(), uuid())


class TaskDefinition(object):
    """
    Defines a Task :)

    Attributes:
        name (str): Task import name.
        image (str): Task image.
        id (str): Task id. If None, an id will be autogenerated.
        upstream (str): Upstream connection string. Defaults to None.
        inputs (dict): Input values
        meta (dict): Freeform metadata
        env (dict): Environment variables
        ports (dict): Port forwards
        routes (dict): HTTP Ingresses
        volumes (dict): List of volumes
        cpu (str): CPU allocation
        memory (str): Memory allocation
        owner (str): Owner name
        created_at (DateTime): Creation date
    """

    def __init__(
        self,
        name:      str,
        image:     str,
        id:        str = None,
        upstream:  str = None,
        parent:    str = None,
        inputs:    dict = {},
        meta:      dict = {},
        env:       dict = {},
        ports:     dict = {},
        routes:    dict = {},
        volumes:   dict = {},
        cpu:       str = '0',
        memory:    str = '0',
        owner:     str = '',
        created_at: datetime = None,
    ):
        """
        Arguments:
            name (str): Task import name.
            image (str): Task image.
            id (str): Task id. If None, an id will be autogenerated.
            upstream (str): Upstream connection string. Defaults to None.
            inputs (dict): Input values
            meta (dict): Freeform metadata
            env (dict): Environment variables
            ports (dict): Port forwards
            routes (dict): HTTP Ingresses
            volumes (dict): List of volumes
            cpu (str): CPU allocation
            memory (str): Memory allocation
            owner (str): Owner name
            created_at (DateTime): Creation date
        """
        self.id = generate_task_id(name) if not id else id
        self.name = name
        self.image = image
        self.parent = parent
        self.upstream = upstream
        self.inputs = inputs
        self.meta = meta
        self.env = env
        self.ports = ports
        self.routes = routes
        self.cpu = cpu
        self.memory = memory
        self.owner = owner
        self.volumes = volumes

        if created_at is None:
            self.created_at = datetime.now(timezone.utc)
        elif isinstance(created_at, datetime):
            self.created_at = created_at
        elif isinstance(created_at, str):
            self.created_at = datetime.fromisoformat(created_at)
        else:
            raise TypeError(f'Expected created_at to be None or datetime, got {created_at}')

    def serialize(self) -> dict:
        """ Serialize task definition to a dict """
        return TaskDefinitionSchema().dump(self)

    @staticmethod
    def deserialize(taskdef: dict) -> TaskDefinition:
        """ Deserialize task definition from a dict """
        return TaskDefinitionSchema().load(taskdef)


class TaskDefinitionSchema(Schema):
    """ TaskDefinition serialization schema. """

    id = fields.Str(required=True)
    name = fields.Str(required=True)
    image = fields.Str(required=True)
    upstream = fields.Str(allow_none=True)
    parent = fields.Str(allow_none=True)
    inputs = fields.Dict(missing={})
    meta = fields.Dict(missing={})
    env = fields.Dict(missing={})
    ports = fields.Dict(missing={})
    routes = fields.Dict(missing={})
    cpu = fields.Str(missing='0')
    memory = fields.Str(missing='0')
    owner = fields.Str(missing='')
    status = fields.Str(allow_none=True)
    error = fields.Str(allow_none=True)
    result = fields.Raw(allow_none=True)
    log = fields.Str(allow_none=True)
    created_at = fields.DateTime('iso', default=lambda: datetime.now(timezone.utc))
    volumes = fields.Mapping(
        keys=fields.Str(),
        values=fields.Mapping(),
        missing={}
    )

    @post_load
    def make_taskdef(self, data: dict, **kwargs) -> TaskDefinition:
        return TaskDefinition(**data)
