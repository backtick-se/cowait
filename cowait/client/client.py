from cowait.engine import ClusterProvider
from cowait.tasks import TaskDefinition, TaskError
from cowait.tasks.messages import TASK_INIT, TASK_LOG, TASK_FAIL, TASK_RETURN, TASK_STATUS


class Client(object):
    def __init__(self, cluster: ClusterProvider):
        self.cluster = cluster

    def run(self, taskdef: TaskDefinition):
        task = self.cluster.spawn(taskdef)

        events = ClientTaskHandler(task)
        for event in self.cluster.logs(task.id):
            events.handle(event)

        # verify that the task exited successfully
        if not events.exit_ok:
            raise TaskError('Task finished without returning - considering it lost')

        return events.result

class TaskEventHandler(object):
    def __init__(self, root):
        self.root = root

    def handle(self, msg):
        if 'type' not in msg:
            return
        type = msg['type']
        if type == TASK_INIT:
            self.on_init(**msg)
        elif type == TASK_RETURN:
            self.on_return(**msg)
        elif type == TASK_FAIL:
            self.on_fail(**msg)
        elif type == TASK_STATUS:
            self.on_status(**msg)
        elif type == TASK_LOG:
            self.on_log(**msg)

    def on_init(self, id, task, **msg):
        pass

    def on_return(self, id, result, result_type, **msg):
        pass

    def on_fail(self, id, error, **msg):
        pass

    def on_status(self, id, status, **msg):
        pass

    def on_log(self, id, data, file):
        pass


class ClientTaskHandler(TaskEventHandler):
    def __init__(self, root):
        super().__init__(root)
        self.result = None
        self.exit_ok = False

    def on_fail(self, ts, id, error, **msg):
        if id == self.root.id:
            raise TaskError(error)

    def on_return(self, ts, id, result, **msg):
        if id == self.root.id:
            self.result = result
            self.exit_ok = True
