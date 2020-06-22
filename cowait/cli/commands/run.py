import sys
import json
import getpass
from cowait.tasks import TaskDefinition
from cowait.engine.errors import TaskCreationError, ProviderError
from cowait.utils import parse_task_image_name, EventEmitter
from cowait.tasks.messages import TASK_INIT, TASK_STATUS, TASK_FAIL, TASK_RETURN, TASK_LOG
from ..config import CowaitConfig
from ..context import CowaitContext
from ..utils import ExitTrap, printheader
from .build import build as build_cmd


def run(
    config: CowaitConfig,
    task: str,
    name: str = None,
    inputs: dict = {},
    env: dict = {},
    ports: dict = {},
    routes: dict = {},
    build: bool = False,
    upstream: str = None,
    detach: bool = False,
    cpu: str = '0',
    memory: str = '0',
    raw: bool = False,
    quiet: bool = False,
):
    logger = RunLogger(raw, quiet)
    try:
        context = CowaitContext.open()
        cluster_name = context.get('cluster', config.default_cluster)
        cluster = config.get_cluster(cluster_name)

        # figure out image name
        remote_image = True
        image, task = parse_task_image_name(task, None)
        if image is None:
            if build:
                build_cmd()
            image = context.get_image_name()
            remote_image = False

        volumes = context.get('volumes', {})
        if not isinstance(volumes, dict):
            raise TaskCreationError('Invalid volume configuration')
        if not remote_image:
            volumes['/var/task'] = {
                'bind': {
                    'src': context.root_path,
                    'mode': 'rw',
                },
            }

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
            parent=None,  # root task
            upstream=context.coalesce('upstream', upstream, agent),
            owner=getpass.getuser(),
            volumes=volumes,
            memory=memory,
            cpu=cpu,
        )

        logger.print_info(taskdef, cluster_name)

        # print execution info

        # submit task to cluster
        task = cluster.spawn(taskdef)

        if detach:
            logger.header('detached')
            return

        def destroy(*args):
            print()
            printheader('interrupt')
            cluster.destroy(task.id)
            sys.exit(1)

        with ExitTrap(destroy):
            # capture & print logs
            logs = cluster.logs(task)
            logger.header('task output')
            for msg in logs:
                logger.handle(msg)

    except ProviderError as e:
        print('Provider error:', str(e))
        logger.on_exception(f'Provider Error: {e}')

    except TaskCreationError as e:
        logger.on_exception(f'Error creating task: {e}')

    finally:
        logger.header()


class RunLogger(EventEmitter):
    def __init__(self, raw: bool = False, quiet: bool = False):
        super().__init__()
        self.on(TASK_INIT, self.on_init)
        self.on(TASK_STATUS, self.on_status)
        self.on(TASK_FAIL, self.on_fail)
        self.on(TASK_RETURN, self.on_return)
        self.on(TASK_LOG, self.on_log)

        self.raw = raw
        self.quiet = quiet

    def handle(self, msg):
        if self.quiet:
            # only top level return value
            if 'type' in msg and msg['type'] == TASK_RETURN and msg['id'] == self.id:
                print(json.dumps(msg['result']))
            return
        elif self.raw:
            print(json.dumps(msg))
        else:
            self.emit_sync(**msg)

    def header(self, title: str = None):
        if self.quiet or self.raw:
            return
        printheader(title)

    def print_info(self, taskdef, cluster_name):
        self.id = taskdef.id

        self.header('task')
        self.print('   task:      ', taskdef.id)
        self.print('   cluster:   ', cluster_name)
        if taskdef.upstream:
            self.print('   upstream:  ', taskdef.upstream)
        self.print('   image:     ', taskdef.image)
        self.print('   inputs:    ', taskdef.inputs)
        self.print('   env:       ', taskdef.env)
        self.print('   volumes:   ', taskdef.volumes)

    def print(self, *args, **kwargs):
        if self.quiet or self.raw:
            return
        print(*args, **kwargs)

    def on_init(self, task: dict, **msg):
        self.print('~~ create', task['id'], 'from', task['image'], task['inputs'])

    def on_status(self, id, status, **msg):
        self.print('~~', id, 'changed status to', status)

    def on_exception(self, error):
        self.header('error')
        self.print(error)

    def on_fail(self, id, error, **msg):
        self.on_exception(f'Task {id} failed:\n{error}')

    def on_return(self, id, result, **msg):
        self.print('~~', id, 'returned:', json.dumps(result, indent=2))

    def on_log(self, id, file, data, **msg):
        self.print(data, end='')
