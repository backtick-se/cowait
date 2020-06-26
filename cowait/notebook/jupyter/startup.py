import random
import asyncio
from cowait.tasks import Task

__task__ = None
__node__ = None


class KernelTask(Task):
    pass


async def __init_kernel_task__():
    from cowait.tasks import TaskDefinition
    from cowait.worker import env_get_cluster_provider, env_get_task_definition
    from cowait.worker.worker_node import WorkerNode
    from cowait.network import get_local_connstr
    global __task__, __node__

    cluster = env_get_cluster_provider()
    parent = env_get_task_definition()

    # create a virtual task for the kernel
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

    # set up a node
    node = WorkerNode(
        id=taskdef.id,
        upstream=taskdef.upstream,
        port=random.randint(10000, 60000),
        quiet=True,
    )
    await node.connect()
    await node.parent.send_init(taskdef)
    node.http.auth.enabled = False
    node.serve()

    # instantiate kernel task
    kernel = KernelTask(node=node, cluster=cluster, taskdef=taskdef)
    await node.parent.send_run()
    await node.parent.send_log(data='Kernel task ready.', file='stdout')

    # write globals
    __node__ = node
    __task__ = kernel

asyncio.get_event_loop().create_task(__init_kernel_task__())
