from pipeline.tasks import Task, TaskDefinition


class ContainerTask(Task):
    async def run(self, name, image, routes: dict = {}):
        taskdef = TaskDefinition(
            name=name,
            image=image,
            env=self.env,
            ports=self.ports,
            parent=self.id,

            routes=routes,
        )

        task = self.cluster.spawn(taskdef)
        await self.watch(task)

    async def watch(self, task):
        logs = self.cluster.logs(task)
        for log in logs:
            print(log)
