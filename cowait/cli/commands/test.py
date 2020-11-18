import sys
from cowait.tasks import TaskDefinition, TASK_LOG
from cowait.engine import ProviderError, TaskCreationError
from ..config import Config
from ..context import Context
from ..utils import ExitTrap
from ..logger import Logger
from .build import build as run_build
from .push import push as run_push


def test(
    config: Config,
    push: bool,
    cluster_name: str = None,
):
    logger = TestLogger()
    try:
        context = Context.open(config)
        cluster = context.get_cluster(cluster_name)

        if push:
            run_push()
        else:
            run_build(config)

        # execute the test task within the current image
        task = cluster.spawn(TaskDefinition(
            name='cowait.test',
            image=context.image,
        ))

        def destroy(*args):
            logger.header('interrupt')
            cluster.destroy(task.id)
            sys.exit(1)

        with ExitTrap(destroy):
            # capture & print logs
            logs = cluster.logs(task)
            logger.header('task output')
            for msg in logs:
                logger.handle(msg)

        logger.header()

        # grab task result
        passing = cluster.wait(task)
        sys.exit(0 if passing else 1)

    except ProviderError as e:
        logger.print_exception(f'Provider Error: {e}')
        sys.exit(1)

    except TaskCreationError as e:
        logger.print_exception(f'Error creating task: {e}')
        sys.exit(1)


class TestLogger(Logger):
    def handle(self, msg):
        type = msg.get('type', None)
        if type == TASK_LOG:
            print(msg['data'], end='')
