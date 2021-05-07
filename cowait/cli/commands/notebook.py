import os
import sys
import time
import getpass
import platform
import traceback
import subprocess
from kubernetes import client
from cowait.cli.utils import ExitTrap
from cowait.cli.context import Context
from cowait.cli.commands.run import RunLogger, run as run_cmd
from cowait.tasks import TaskDefinition
from cowait.utils import uuid


def notebook(config, image: str = None, cluster_name: str = None) -> None:
    context = Context.open(config)

    if not context.notebook:
        print('Notebook funcitonaility is not enabled.')
        print('To enable, set features.notebook to True in cowait.yml and rebuild.')
        sys.exit(1)

    if image is not None:
        print('Remote images are currently not supported')
        sys.exit(1)

    volumes = {
        '/var/task': {
            'bind': {
                'src': os.getcwd(),
                'mode': 'rw',
                'inherit': 'same-image',
            },
        }
    }

    cluster = context.get_cluster(cluster_name)

    # Docker
    if cluster.type == 'docker':
        return run_cmd(
            config=config,
            task='cowait.notebook',
            build=False,
            image=image,
            routes={
                '/': '8888',
            },
            cluster_name=cluster_name,
            volumes=volumes,
        )

    # check for clientfs
    clientfs_executable = './clientfs-' + platform.system().lower()
    if not os.path.exists(clientfs_executable):
        print('Kubernetes notebooks are not supported in this build of Cowait')
        sys.exit(1)

    # Kubernetes
    core = client.CoreV1Api()
    notebook_id = 'notebook-' + uuid(4)

    core.create_namespaced_persistent_volume_claim(
        namespace=cluster.namespace,
        body=client.V1PersistentVolumeClaim(
            metadata=client.V1ObjectMeta(
                name=notebook_id,
                namespace=cluster.namespace,
            ),
            spec=client.V1PersistentVolumeClaimSpec(
                storage_class_name='clientfs',
                access_modes=['ReadWriteMany'],
                resources=client.V1ResourceRequirements(
                    requests={
                        'storage': '1G',
                    },
                ),
            ),
        ),
    )

    def delete_pvc(task_id):
        print('destroy', task_id)
        if task_id != notebook_id:
            return

        print('* stopping clientfs')
        clientfs.terminate()

        print('* deleting volume')
        core.delete_namespaced_persistent_volume_claim(notebook_id, cluster.namespace)

    cluster.on('kill', delete_pvc)

    pvc_id = None

    while True:
        time.sleep(1)
        volume = core.read_namespaced_persistent_volume_claim(notebook_id, cluster.namespace)
        if volume.status.phase == 'Bound':
            pvc_id = 'pvc-' + volume.metadata.uid
            print('* created volume', notebook_id, '/', pvc_id)
            break

    volumes['/var/task'] = {
        'persistent_volume_claim': {
            'claim_name': notebook_id,
        },
    }

    # start clientfs
    clientfs_host = cluster.args.get('clientfs', {}).get('host')
    print(f'* connecting clientfs volume to {clientfs_host}...')
    clientfs = subprocess.Popen([
        clientfs_executable,
        f"--proxy={clientfs_host}",
        f"--volume={pvc_id}"
    ])

    logger = RunLogger()
    try:
        # default to agent as upstream
        agent = cluster.find_agent()

        # create task definition
        taskdef = TaskDefinition(
            id=notebook_id,
            name='cowait.notebook',
            image=context.image,
            env={
                **context.extend('environment', {}),
                **context.dotenv,
            },
            routes={
                '/': '8888',
            },
            parent=None,  # root task
            upstream=agent,
            owner=getpass.getuser(),
            volumes=context.extend('volumes', volumes),
        )

        # print execution info
        logger.print_info(taskdef, cluster)

        # submit task to cluster
        task = cluster.spawn(taskdef)

        detach = False
        if detach:
            logger.header('detached')
            return

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

    except Exception:
        traceback.print_exc()
        sys.exit(1)


def run_notebook(
    config, path: str,
    image: str, cluster: str, name: str, inputs: dict, env: dict,
    build: bool, detach: bool, quiet: bool
):
    run_cmd(
        config,
        task='cowait.tasks.notebook',
        name=name,
        image=image,
        inputs={
            **inputs,
            'path': path
        },
        env=env,
        ports={},
        routes={},
        build=build,
        detach=detach,
        quiet=quiet,
        cluster_name=cluster,
    )
