from cowait.tasks import TASK_LOG
from cowait.worker.logger import Logger
from IPython.core.display import display, HTML


class HTMLLogger(Logger):
    def log(self, type: str, msg: dict) -> None:
        if type == TASK_LOG:
            self.log_output(**msg)

    def log_output(self, id, file, data, **msg):
        display(HTML(f'<pre>{id}: {data}</pre>'))
