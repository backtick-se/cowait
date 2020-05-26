import sys
from cowait.tasks import TaskDefinition
from cowait.engine.errors import TaskCreationError, ProviderError
from cowait.utils.const import DEFAULT_BASE_IMAGE
from cowait.utils import uuid
from ..errors import CliError
from ..config import CowaitConfig
from ..context import CowaitContext
from ..utils import ExitTrap, printheader


def agent(
    config: CowaitConfig,
    detach: bool = False,
    upstream: str = None,
) -> None:
    try:
        context = CowaitContext.open()
        cluster_name = context.get('cluster', config.default_cluster)
        cluster = config.get_cluster(cluster_name)

        if cluster.type == 'api':
            raise CliError('Error: Cant deploy agent using an API cluster')

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
                'http_token': uuid(),
            },
        )

        # submit task to cluster
        task = cluster.spawn(taskdef)

        if detach:
            printheader('detached')
            return

        def destroy(*args):
            print()
            printheader('interrupt')
            cluster.destroy(task.id)
            sys.exit(0)

        with ExitTrap(destroy):
            # capture & print logs
            logs = cluster.logs(task)
            printheader('task output')
            for log in logs:
                print(log, flush=True)

        printheader()

    except ProviderError as e:
        raise CliError(f'Provider error: {e}')

    except TaskCreationError as e:
        raise CliError(f'Task creation error: {e}')
