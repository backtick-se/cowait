"""
Task Worker entry point.

Environment:
    TASK_CLUSTER (json): JSON-serialized ClusterProvider
    TASK_DEFINITION (json): JSON-serialized TaskDefinition
"""
import pipeline.worker
from pipeline.tasks import TaskDefinition, TaskContext
from pipeline.worker.connector import LoggingConnector, PushConnector
from pipeline.worker.env import env_get_cluster_provider, env_get_task_definition


if __name__ == '__main__':
    # unpack cluster provider
    cluster = env_get_cluster_provider()

    # unpack task definition
    taskdef = env_get_task_definition()

    # upstream handler
    if taskdef.parent:
        upstream = PushConnector(taskdef.id, taskdef.parent)
    else:
        upstream = LoggingConnector(taskdef.id)

    # execute task
    pipeline.worker.execute(cluster, upstream, taskdef)
