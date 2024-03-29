from __future__ import annotations
from datetime import datetime, timezone
from ..utils import uuid


def generate_task_id(name: str, unique: bool = True) -> str:
    """
    Generates a new Task ID from a task import path.

    Args:
        name (str): Task import path name
        unique (bool): True if the ID should be unique. Adds a random string

    Returns:
        id (str): Task ID
    """

    if '.' in name:
        dot = name.rfind('.')
        name = name[dot+1:]

    name = name.replace('.', '-')
    name = name.replace('_', '-')

    if unique:
        return '%s-%s' % (name.lower(), uuid())
    else:
        return name.lower()


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
        cpu (str): CPU request
        cpu_limit (str): CPU limit
        memory (str): Memory request
        memory_limit (str): Memory limit
        affinity (str): Node affinity
        nodes (dict): Node selector labels
        owner (str): Owner name
        created_at (DateTime): Creation date
    """

    def __init__(
        self,
        name:         str,
        image:        str,
        id:           str = None,
        upstream:     str = None,
        parent:       str = None,
        inputs:       dict = None,
        meta:         dict = None,
        env:          dict = None,
        ports:        dict = None,
        routes:       dict = None,
        volumes:      dict = None,
        cpu:          str = None,
        cpu_limit:    str = None,
        memory:       str = None,
        memory_limit: str = None,
        affinity:     str = None,
        nodes:        dict = None,
        owner:        str = None,
        created_at:   datetime = None,
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
            cpu (str): CPU request
            cpu_limit (str): CPU limit. Defaults to cpu request if unset.
            memory (str): Memory request
            memory_limit (str): Memory limit. Defaults to memory request if unset
            affinity (str): Affinity Mode (None/stack/spread)
            owner (str): Owner name
            created_at (DateTime): Creation date
        """
        self.id = generate_task_id(name) if id is None else id
        self.name = name
        self.image = image
        self.parent = parent
        self.upstream = upstream
        self.inputs = inputs or {}
        self.meta = meta or {}
        self.env = env or {}
        self.ports = ports or {}
        self.routes = routes or {}
        self.cpu = cpu
        self.memory = memory
        self.cpu_limit = cpu_limit or cpu
        self.memory_limit = memory_limit or memory
        self.owner = owner or ''
        self.volumes = volumes or {}
        self.affinity = affinity
        self.nodes = nodes or {}

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
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'upstream': self.upstream,
            'parent': self.parent,
            'inputs': self.inputs,
            'meta': self.meta,
            'env': self.env,
            'ports': self.ports,
            'routes': self.routes,
            'cpu': self.cpu,
            'cpu_limit': self.cpu_limit,
            'memory': self.memory,
            'memory_limit': self.memory_limit,
            'affinity': self.affinity,
            'nodes': self.nodes,
            'owner': self.owner,
            'created_at': self.created_at.isoformat(),
            'volumes': self.volumes,
        }

    @staticmethod
    def deserialize(taskdef: dict) -> TaskDefinition:
        """ Deserialize task definition from a dict """
        return TaskDefinition(
            id=taskdef.get('id'),
            name=taskdef.get('name'),
            image=taskdef.get('image'),
            upstream=taskdef.get('upstream', None),
            parent=taskdef.get('parent', None),
            inputs=taskdef.get('inputs', {}),
            meta=taskdef.get('meta', {}),
            env=taskdef.get('env', {}),
            ports=taskdef.get('ports', {}),
            routes=taskdef.get('routes', {}),
            cpu=taskdef.get('cpu', None),
            cpu_limit=taskdef.get('cpu_limit', None),
            memory=taskdef.get('memory', None),
            memory_limit=taskdef.get('memory_limit', None),
            affinity=taskdef.get('affinity', None),
            nodes=taskdef.get('nodes', {}),
            owner=taskdef.get('owner', None),
            created_at=datetime.fromisoformat(taskdef.get(
                'created_at', datetime.now().isoformat())),
            volumes=taskdef.get('volumes', {}),
        )
