from pipeline.tasks import Task, TaskDefinition


class ContainerTask(Task):
    async def run(self, name, image):
        taskdef = TaskDefinition(
            name=name,
            image=image,
            env=self.env,
            ports=self.ports,
            parent=self.id,
        )

        task = self.cluster.spawn(taskdef)

        logs = self.cluster.logs(task)
        for log in logs:
            print(log)
