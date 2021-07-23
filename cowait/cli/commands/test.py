import sys
import getpass
from cowait.tasks import TaskDefinition, TASK_LOG
from cowait.engine import ProviderError, TaskCreationError
from ..config import Config
from ..context import Context
from ..utils import ExitTrap
from ..logger import Logger


def test(
    config: Config,
    cluster_name: str = None,
    mount: bool = True,
    cpu: str = None,
    cpu_limit: str = None,
    memory: str = None,
    memory_limit: str = None,
    marks: str = None,
    verbose: bool = None,
    capture: bool = None,
):
    logger = TestLogger()
    try:
        context = Context.open(config)
        cluster = context.get_cluster(cluster_name)

        volumes = {}
        if mount and cluster.type == 'docker':
            # when testing in docker, mount the local directory
            # this avoids the problem of having to constantly rebuild in order to test
            print('** Mounting', context.root_path)
            volumes['/var/task'] = {
                'bind': {
                    'src': context.root_path,
                    'mode': 'rw',
                    'inherit': 'same-image',
                },
            }

        # execute the test task within the current image
        task = cluster.spawn(TaskDefinition(
            name='cowait.test',
            image=context.image,
            owner=getpass.getuser(),
            env={
                **context.environment,
                **context.dotenv,
            },
            volumes={
                **context.get('volumes', {}),
                **volumes,
            },
            inputs={
                'marks': marks,
                'verbose': verbose,
                'capture': capture,
            },
            cpu=context.override('cpu', cpu),
            cpu_limit=context.override('cpu_limit', cpu_limit),
            memory=context.override('memory', memory),
            memory_limit=context.override('memory_limit', memory_limit),
        ))

        def destroy(*args):
            logger.header('interrupt')
            cluster.destroy(task.id)
            sys.exit(1)

        with ExitTrap(destroy):
            # capture & print logs
            logs = cluster.logs(task.id)
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
