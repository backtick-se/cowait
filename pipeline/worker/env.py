import os
import json
from pipeline.tasks import TaskDefinition
from pipeline.engine import get_cluster_provider, ENV_TASK_CLUSTER, ENV_TASK_DEFINITION


def env_get_cluster_provider():
    if not ENV_TASK_CLUSTER in os.environ:
        raise RuntimeError(f'Cluster provider must be passed in the {ENV_TASK_CLUSTER} environment variable.')

    provider_json = json.loads(os.environ[ENV_TASK_CLUSTER])
    return get_cluster_provider(**provider_json)


def env_get_task_definition():
    if not ENV_TASK_DEFINITION in os.environ:
        raise RuntimeError(f'Task definition must be passed in the {ENV_TASK_DEFINITION} environment variable.')

    taskdef_json = json.loads(os.environ[ENV_TASK_DEFINITION])
    return TaskDefinition.deserialize(taskdef_json)