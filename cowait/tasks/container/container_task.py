from cowait.tasks import Task, TaskDefinition


class ContainerTask(Task):
    async def run(
        self, name: str, image: str, env: dict = {},
        routes: dict = {}, ports: dict = {}, meta: dict = {},
        cpu: any = 0, memory: any = 0, affinity: str = None,
        **inputs
    ):
        taskdef = TaskDefinition(
            name=name,
            image=image,
            parent=self.id,
            owner=self.taskdef.owner,
            inputs=inputs,
            ports=ports,
            routes=routes,
            cpu=cpu,
            memory=memory,
            affinity=affinity,
            env={
                **self.taskdef.env,
                **env,
            },
            meta={
                **self.taskdef.meta,
                **meta,
            },
        )

        # run it
        task = self.cluster.spawn(taskdef)

        # wait for container to exit
        await self.watch(task)

        # clean up
        self.cluster.destroy(task.id)

    async def watch(self, task):
        logs = self.cluster.logs(task.id)
        for log in logs:
            print(log)
