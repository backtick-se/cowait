import os
import json
from cowait.tasks import TaskDefinition
from cowait.engine import get_cluster_provider, env_unpack, \
    ENV_TASK_CLUSTER, ENV_TASK_DEFINITION, ENV_GZIP_ENABLED


def env_get(key):
    if key not in os.environ:
        raise ValueError(f'Missing required environment variable {key}')
    value = os.environ[key]
    if os.getenv(ENV_GZIP_ENABLED, '0') == '1':
        return env_unpack(value)
    return json.loads(value)


def env_get_cluster_provider():
    clusterdef = env_get(ENV_TASK_CLUSTER)
    return get_cluster_provider(**clusterdef)


def env_get_task_definition():
    taskdef = env_get(ENV_TASK_DEFINITION)
    return TaskDefinition.deserialize(taskdef)
