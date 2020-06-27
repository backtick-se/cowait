import cowait
import asyncio

__task__ = None
__node__ = None


class KernelTask(cowait.Task):
    pass


async def __init_kernel_task__():
    global __task__, __node__
    import os
    from cowait.tasks import TaskDefinition
    from cowait.network import get_local_connstr
    from cowait.worker import env_get_cluster_provider, env_get_task_definition
    from cowait.notebook.node import NotebookNode

    cluster = env_get_cluster_provider()
    parent = env_get_task_definition()
    token = os.getenv('KERNEL_TOKEN')

    taskdef = TaskDefinition(
        name='kernel',
        image=parent.image,
        parent=parent.id,
        volumes=parent.volumes,
        env=parent.env,
        upstream=get_local_connstr(),
        meta={
            'virtual': True,
        },
    )

    # set up notebook node
    node = NotebookNode(taskdef)
    await node.start(token)

    # instantiate kernel task
    kernel = KernelTask(node=node, cluster=cluster, taskdef=taskdef)

    # write globals
    __node__ = node
    __task__ = kernel

asyncio.get_event_loop().create_task(__init_kernel_task__())
