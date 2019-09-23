"""
Task Worker entry point.

Environment:
    TASK_CLUSTER (json): JSON-serialized ClusterProvider
    TASK_DEFINITION (json): JSON-serialized TaskDefinition
"""
import pipeline.worker
from pipeline.tasks import TaskContext
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
    """ Root task node setup """
    node.attach(TaskList())

    if taskdef.upstream:
        print('root: connecting upstream')
        node.connect(taskdef.upstream)
    else:
        node.attach(FlowLogger())


def create_child_node(node, taskdef):
    """ Child task node setup """
    print('child: connecting upstream')
    node.connect(taskdef.upstream)


def create_node(taskdef):
    node = Node(taskdef.id)
    if not taskdef.parent:
        create_root_node(node, taskdef)
    else:
        create_child_node(node, taskdef)
    return node



if __name__ == '__main__':
    main()
