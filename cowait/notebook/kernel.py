import os
import asyncio
from ipykernel.kernelapp import IPKernelApp
from ipykernel.ipkernel import IPythonKernel
from cowait.tasks import Task, TaskDefinition
from cowait.network import get_local_url
from cowait.storage import StorageBackends
from cowait.worker import env_get_cluster_provider, env_get_task_definition
from .node import NotebookNode

import cowait.notebook.html_repr  # noqa: F401

ENV_KERNEL_TOKEN = 'COWAIT_KERNEL_TOKEN'


class KernelTask(Task):
    pass


class CowaitKernel(IPythonKernel):
    def start(self):
        super().start()
        asyncio.get_event_loop().create_task(self.init_node())

    async def init_node(self):
        cluster = env_get_cluster_provider()
        parent = env_get_task_definition()
        token = os.getenv(ENV_KERNEL_TOKEN)

        taskdef = TaskDefinition(
            name='kernel',
            image=parent.image,
            parent=parent.id,
            volumes=parent.volumes,
            storage=parent.storage,
            env=parent.env,
            upstream=get_local_url(),
            meta={
                'virtual': True,
            },
        )

        # set up notebook node
        self.node = NotebookNode(taskdef)
        await self.node.start(token)

        # instantiate kernel task
        self.task = KernelTask(node=self.node, cluster=cluster, taskdef=taskdef)
        setattr(self.task, 'storage', StorageBackends(taskdef.storage))

        # write globals
        self.shell.push({
            'kernel': self.task,
            'tasks': self.task.subtasks,
        })

    def do_shutdown(self, restart):
        asyncio.get_event_loop().create_task(self.shutdown_node())
        super().do_shutdown(restart)

    async def shutdown_node(self):
        await self.node.stop()
        self.node = None
        self.task = None


if __name__ == '__main__':
    app = IPKernelApp.instance(kernel_class=CowaitKernel)
    app.initialize()
    app.start()
