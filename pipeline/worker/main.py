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
from pipeline.network import Node
from pipeline.network.service import FlowLogger, TaskList


def main():
    # unpack cluster provider
    cluster = env_get_cluster_provider()

    # unpack task definition
    taskdef = env_get_task_definition()

    # create network node
    node = create_node(taskdef)

    # execute task
    pipeline.worker.execute(cluster, node, taskdef)


def create_root_node(node, taskdef):
    node.attach(TaskList())
    node.attach(FlowLogger())


def create_child_node(node, taskdef):
    node.connect(taskdef.upstream)


def create_node(taskdef):
    node = Node(taskdef.id)
    if not taskdef.upstream:
        create_root_node(node, taskdef)
    else:
        create_child_node(node, taskdef)
    return node



if __name__ == '__main__':
    main()
