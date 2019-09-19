import os
import time
import json
import kubernetes
from typing import Dict
from kubernetes import client, config, watch
from pipeline.tasks import Task, TaskContext, TaskDefinition
from .cluster import ClusterProvider


class KubernetesTask(Task):
    def __init__(self, cluster: ClusterProvider, taskdef: TaskDefinition, job, pod):
        super().__init__(TaskContext(
            cluster=cluster,
            taskdef=taskdef,
            upstream=None,
        ))
        self.job = job
        self.pod = pod


class KubernetesProvider(ClusterProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # hacky way to check if we're running within a pod
        if 'TASK_CLUSTER_PROVIDER' in os.environ:
            config.load_incluster_config()
        else:
            config.load_kube_config()

        configuration = client.Configuration()
        self.batch = client.BatchV1Api(kubernetes.client.ApiClient(configuration))
        self.core = client.CoreV1Api(kubernetes.client.ApiClient(configuration))


    def spawn(self, taskdef: TaskDefinition) -> KubernetesTask:
        # container definition
        container = client.V1Container(
            name=taskdef.id,
            image=taskdef.image, 
            image_pull_policy='Always',
            env=kube_env_list({
                **taskdef.env,
                'TASK_CLUSTER_PROVIDER': 'kubernetes',
                'TASK_INPUTS': json.dumps(taskdef.inputs),
                'TASK_CONFIG': json.dumps(taskdef.config),
            }),
        )

        # job definition
        jobdef = client.V1Job(
            api_version='batch/v1', 
            kind='Job',
            status=client.V1JobStatus(),
            metadata=client.V1ObjectMeta(
                namespace=taskdef.namespace, 
                name=taskdef.id,
            ),
            spec=client.V1JobSpec(
                backoff_limit=0,
                ttl_seconds_after_finished=600, 
                template=client.V1PodTemplateSpec(
                    spec=client.V1PodSpec(
                        containers=[ container ], 
                        restart_policy='Never'
                    ),
                ),
            ),
        )

        # create job
        job = self.batch.create_namespaced_job(taskdef.namespace, jobdef)
        while True:
            pod = self.get_job_pod(job)
            if pod.status.phase != 'Pending':
                break
            time.sleep(0.5)

        # wrap & return task
        print('spawned kubenetes pod with name', pod.metadata.name)
        return KubernetesTask(self, taskdef, job, pod)


    def get_job_pod(self, job):
        res = self.core.list_namespaced_pod(
            namespace=job.metadata.namespace,
            label_selector='controller-uid=' + job.spec.selector.match_labels['controller-uid']
        )
        if len(res.items) < 1:
            raise RuntimeError('Could not find job pod')

        return res.items[0]


    def wait(self, task: KubernetesTask) -> None:
        while True:
            res = self.batch.read_namespaced_job(
                name=task.job.metadata.name,
                namespace=task.job.metadata.namespace,
            )

            if res.status.failed:
                raise RuntimeError('Task failed')

            if res.status.succeeded:
                break

            time.sleep(0.5)


    def logs(self, task: KubernetesTask):
        w = watch.Watch()
        return w.stream(
            self.core.read_namespaced_pod_log, 
            name=task.pod.metadata.name, 
            namespace=task.pod.metadata.namespace,
        )



def kube_env_list(env: Dict) -> list:
    """ creates a kubernetes environment list from a dictionary """
    env_list = [ ]
    for name, value in env.items():
        env_list.append(client.V1EnvVar(name, value))
    return env_list
