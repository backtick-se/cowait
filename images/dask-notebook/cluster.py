import os
import json
from dask_kubernetes import KubeCluster
from kubernetes_asyncio import client

# load task definition from environment
task = json.loads(os.environ['TASK_DEFINITION'])


def create_cluster(**kwargs):
    workers = task['inputs'].get('workers', 0)
    cores = task['inputs'].get('worker_cores', 2)
    memory = task['inputs'].get('worker_memory', 2)
    image = task['inputs'].get('worker_image', 'daskdev/dask:latest')

    container = client.V1Container(
        name='dask',
        image=image,
        args=[
            'dask-worker',
            '--nthreads', str(cores),
            '--no-bokeh',
            '--memory-limit', f'{memory}GB'
            '--death-timeout', '60',
        ],
        resources=client.V1ResourceRequirements(
            limits={
                'cpu': str(cores),
                'memory': f'{memory}G',
            },
            requests={
                'cpu': str(cores),
                'memory': f'{memory}G',
            },
        ),
    )

    pod = client.V1Pod(
        metadata=client.V1ObjectMeta(
            labels={
                'pipeline/task': task.get('id'),
                'pipeline/parent': task.get('parent', ''),
            },
        ),
        spec=client.V1PodSpec(
            restart_policy='Never',
            image_pull_secrets=[
                client.V1LocalObjectReference(name=secret)
                for secret in task['inputs'].get('pull_secrets', ['docker'])
            ],
            containers=[container],
        ),
    )

    return KubeCluster(
        pod_template=pod,
        n_workers=workers,
    )
