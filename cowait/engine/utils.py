import json
import gzip
from base64 import b64encode, b64decode
from cowait.tasks import TaskDefinition
from .const import ENV_TASK_CLUSTER, ENV_TASK_DEFINITION, ENV_GZIP_ENABLED


def env_pack(value):
    value = json.dumps(value).encode('utf-8')
    value = gzip.compress(value)
    return b64encode(value).decode('utf-8')


def env_unpack(value):
    value = b64decode(value)
    value = gzip.decompress(value)
    return json.loads(value)


def base_environment(cluster, taskdef: TaskDefinition) -> dict:
    """
    Create a container environment dict from a task definition.

    Arguments:
        taskdef (TaskDefinition): Task definition

    Returns:
        env (dict): Environment variable dict
    """

    return {
        **taskdef.env,
        ENV_GZIP_ENABLED:    '1',
        ENV_TASK_CLUSTER:    env_pack(cluster.serialize()),
        ENV_TASK_DEFINITION: env_pack(taskdef.serialize()),
    }

