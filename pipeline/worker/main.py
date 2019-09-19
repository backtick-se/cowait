"""
Worker Bootstrap
"""
import os
import sys
import json
import pipeline.worker
from pipeline.engine import get_cluster_provider
from pipeline.tasks import TaskDefinition, TaskContext
from pipeline.worker.connector import LoggingConnector, UpstreamConnector

if __name__ == '__main__':
    # unpack cluster provider
    provider_type = os.environ['TASK_CLUSTER_PROVIDER']
    provider_args = json.loads(os.environ['TASK_CLUSTER_ARGUMENTS'])

    ClusterProvider = get_cluster_provider(provider_type)
    cluster = ClusterProvider(**provider_args)

    # unpack task definition
    taskdef = TaskDefinition.deserialize(json.loads(os.environ['TASK_DEFINITION']))

    # upstream handler
    root_task = taskdef.parent == 'root'
    if root_task:
        upstream = LoggingConnector(taskdef.id)
    else:
        upstream = UpstreamConnector(taskdef.id, taskdef.parent)

    # execute task
    pipeline.worker.execute(cluster, upstream, taskdef)
