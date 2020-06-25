import json
from cowait.engine import ENV_TASK_CLUSTER, ENV_TASK_DEFINITION
from cowait.tasks.shell import ShellTask


class NotebookTask(ShellTask):
    async def run(self, **inputs):
        self.node.http.auth.enabled = False
        await super().run(
            command='jupyter lab',
            env={
                ENV_TASK_DEFINITION: json.dumps(self.serialize()),
                ENV_TASK_CLUSTER: json.dumps(self.cluster.serialize()),
            },
        )
