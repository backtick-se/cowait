import sys
from cowait.tasks import TaskDefinition
from cowait.engine.errors import TaskCreationError, ProviderError
from cowait.utils.const import DEFAULT_BASE_IMAGE
from cowait.utils import uuid
from ..errors import CliError
from ..config import Config
from ..context import Context
from ..utils import ExitTrap
from .run import RunLogger


def agent(
    config: Config,
    detach: bool = False,
    upstream: str = None,
    cluster_name: str = None,
) -> None:
    logger = RunLogger(quiet=False, raw=False)
    try:
        context = Context.open(config)
        cluster = context.get_cluster(cluster_name)

        if cluster.type == 'api':
            raise CliError('Error: Cant deploy agent using an API cluster')

        token = uuid()
        if cluster.type == 'docker':
            token = ''

        cluster.destroy('agent')

        # create task definition
        taskdef = TaskDefinition(
            id='agent',
            name='cowait.tasks.agent',
            image=DEFAULT_BASE_IMAGE,
            upstream=upstream,
            routes={
                '/': 80,
            },
            meta={
                'http_token': token,
            },
        )

        # submit task to cluster
        task = cluster.spawn(taskdef)

        if detach:
            logger.header('detached')
            return

        def destroy(*args):
            logger.header('interrupt')
            cluster.destroy(task.id)
            sys.exit(0)

        with ExitTrap(destroy):
            # capture & print logs
            logs = cluster.logs(task)
            logger.header('task output')
            for log in logs:
                logger.handle(log)

        logger.header()

    except ProviderError as e:
        raise CliError(f'Provider error: {e}')

    except TaskCreationError as e:
        raise CliError(f'Task creation error: {e}')
