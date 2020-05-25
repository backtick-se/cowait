import sys
from cowait.tasks import TaskDefinition
from cowait.engine.errors import TaskCreationError, ProviderError
from cowait.utils.const import DEFAULT_BASE_IMAGE
from cowait.utils import uuid
from ..config import CowaitConfig
from ..context import CowaitContext
from ..utils import ExitTrap, printheader


def agent(
    cluster_name: str = None,
    detach: bool = False,
    upstream: str = None,
) -> None:
    try:
        config = CowaitConfig.load()
        context = CowaitContext.open()

        # setup cluster provider
        if cluster_name is None:
            cluster_name = context.get('cluster', config.default_cluster)
        cluster = config.get_cluster(cluster_name)

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

    except ProviderError as e:
        printheader('error')
        print('Provider error:', str(e))

    except TaskCreationError as e:
        printheader('error')
        print('Error creating task:', str(e))

    finally:
        printheader()
