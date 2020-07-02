import os
import asyncio
from ipykernel.kernelapp import IPKernelApp
from ipykernel.ipkernel import IPythonKernel
from cowait.tasks import Task, TaskDefinition
from cowait.network import get_local_connstr
from cowait.worker import env_get_cluster_provider, env_get_task_definition
from cowait.notebook.node import NotebookNode


class KernelTask(Task):
    def _repr_html_(self):
        return f'<b>kernel task!</b>'


class CowaitKernel(IPythonKernel):
    def start(self):
        super().start()
        asyncio.get_event_loop().create_task(self.init_node())

    async def init_node(self):
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
        self.node = NotebookNode(taskdef)
        await self.node.start(token)

        # instantiate kernel task
        self.task = KernelTask(node=self.node, cluster=cluster, taskdef=taskdef)

        # write globals
        self.shell.push({
            '__node__': self.node,
            '__task__': self.task,
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
