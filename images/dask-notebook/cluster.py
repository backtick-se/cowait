import os
import math
import json
from dask_kubernetes import KubeCluster
from kubernetes_asyncio import client

# load task definition from environment
task = json.loads(os.environ['TASK_DEFINITION'])


def cpu_to_threads(cpu):
    mult = 1
    cpu = str(cpu)
    unit = cpu[-1]
    if unit.isalpha():
        cpu = cpu[:-1]
        if unit == 'm':
            mult = 0.001
    cpu = float(cpu) * mult
    return math.ceil(cpu)


def create_cluster(**kwargs):
    workers = task['inputs'].get('workers', 0)
    cpu = task['inputs'].get('worker_cores', 2)
    memory = task['inputs'].get('worker_memory', 2)
    image = task['inputs'].get('worker_image', 'daskdev/dask:latest')

    container = client.V1Container(
        name='dask',
        image=image,
        args=[
            'dask-worker',
            '--nthreads', str(cpu_to_threads(cpu)),
            '--no-bokeh',
            '--memory-limit', f'{memory}B',
            '--death-timeout', '60',
        ],
        resources=client.V1ResourceRequirements(
            limits={
                'cpu': str(cpu),
                'memory': str(memory),
            },
            requests={
                'cpu': str(cpu),
                'memory': str(memory),
            },
        ),
    )

    pod = client.V1Pod(
        metadata=client.V1ObjectMeta(
            labels={
                'pipeline/task': 'worker-' + task.get('id'),
                'pipeline/parent': task.get('id'),
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
