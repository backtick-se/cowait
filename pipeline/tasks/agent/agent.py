from pipeline.tasks import Task, sleep


class AgentTask(Task):
    async def before(self, inputs: dict) -> None:
        async def dump(**msg):
            print(msg)
        self.node.children.on('*', dump)

        return inputs

    async def run(self, **inputs):
        while True:
            sleep(1.0)
