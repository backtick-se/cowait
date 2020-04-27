from cowait.tasks import Task, TaskDefinition


class ContainerTask(Task):
    async def run(
        self, name: str, image: str, env: dict = {},
        routes: dict = {}, ports: dict = {},
        cpu: any = 0, memory: any = 0,
        **inputs
    ):
        taskdef = TaskDefinition(
            name=name,
            image=image,
            parent=self.id,
            inputs=inputs,
            ports=ports,
            routes=routes,
            cpu=cpu,
            memory=memory,
            env={
                **self.env,
                **env,
            },
        )

        # run it
        task = self.cluster.spawn(taskdef)

        # wait for container to exit
        await self.watch(task)

        # clean up
        self.cluster.destroy(task)

    async def watch(self, task):
        logs = self.cluster.logs(task)
        for log in logs:
            print(log)
