"""
Task Worker entry point.

Environment:
    TASK_CLUSTER (json): JSON-serialized ClusterProvider
    TASK_DEFINITION (json): JSON-serialized TaskDefinition
"""
import pipeline.worker
from pipeline.network import PushSocket, NoopSocket
from pipeline.tasks import TaskDefinition, TaskContext
from pipeline.worker.env import env_get_cluster_provider, env_get_task_definition
from pipeline.flows.client import FlowClient
from pipeline.flows.service import FlowLogger
from pipeline.flows.tasklist import TaskList
from pipeline.network import Node

def main():
    # unpack cluster provider
    cluster = env_get_cluster_provider()

    # unpack task definition
    taskdef = env_get_task_definition()

    # upstream handler
    node = Node(taskdef.id)
    if not taskdef.upstream:
        print('im the root task')
        node.attach(FlowLogger())
        node.attach(TaskList())
    else:
        print('connecting upstream...')
        node.connect(taskdef.upstream)

    # execute task
    print('running task...')
    pipeline.worker.execute(cluster, node, taskdef)


if __name__ == '__main__':
    main()
