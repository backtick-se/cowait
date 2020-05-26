import os
import sys
from cowait.tasks import TaskDefinition
from cowait.engine.errors import TaskCreationError, ProviderError
from cowait.utils import parse_task_image_name
from ..config import CowaitConfig
from ..context import CowaitContext
from ..utils import ExitTrap, printheader
from .build import build as build_cmd


def run(
    config: CowaitConfig,
    task: str,
    name: str = None,
    cluster_name: str = None,
    inputs: dict = {},
    env: dict = {},
    ports: dict = {},
    routes: dict = {},
    build: bool = False,
    upstream: str = None,
    detach: bool = False,
    cpu: str = '0',
    memory: str = '0',
):
    try:
        context = CowaitContext.open()
        cluster_name = context.get('cluster', config.default_cluster)
        cluster = config.get_cluster(cluster_name)

        # figure out image name
        image, task = parse_task_image_name(task, None)
        if image is None:
            if build:
                build_cmd()
            image = context.get_image_name()

        # default to agent as upstream
        agent = cluster.find_agent()

        # create task definition
        taskdef = TaskDefinition(
            id=name,
            name=task,
            image=image,
            inputs=inputs,
            env={
                **context.get('environment', {}),
                **env,
            },
            ports=ports,
            routes=routes,
            upstream=context.coalesce('upstream', upstream, agent),
            parent=None,  # root task
            owner=os.getlogin(),
            cpu=cpu,
            memory=memory,
        )

        # print execution info
        printheader('task')
        print('   task:      ', taskdef.id)
        print('   cluster:   ', cluster_name)
        if taskdef.upstream:
            print('   upstream:  ', taskdef.upstream)
        print('   image:     ', image)
        print('   inputs:    ', inputs)
        print('   env:       ', env)

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
