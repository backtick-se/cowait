import os
import json
from cowait.tasks import TaskDefinition
from cowait.engine import \
    get_cluster_provider, \
    ENV_TASK_CLUSTER, \
    ENV_TASK_DEFINITION


def env_get_cluster_provider():
    if ENV_TASK_CLUSTER not in os.environ:
        raise ValueError(
            f'Cluster provider must be passed in the '
            f'{ENV_TASK_CLUSTER} environment variable.')

    provider_json = json.loads(os.environ[ENV_TASK_CLUSTER])
    return get_cluster_provider(**provider_json)


def env_get_task_definition():
    if ENV_TASK_DEFINITION not in os.environ:
        raise ValueError(
            f'Task definition must be passed in the '
            f'{ENV_TASK_DEFINITION} environment variable.')

    taskdef_json = json.loads(os.environ[ENV_TASK_DEFINITION])
    return TaskDefinition.deserialize(taskdef_json)
