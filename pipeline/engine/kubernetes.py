import os
import time
import kubernetes
from typing import Dict
from kubernetes import client, config, watch
from pipeline.tasks import Task, TaskContext, TaskDefinition
from .const import ENV_TASK_CLUSTER
from .cluster import ClusterProvider


class KubernetesTask(Task):
    def __init__(self, cluster: ClusterProvider, taskdef: TaskDefinition, job, pod):
        super().__init__(TaskContext(
            cluster=cluster,
            taskdef=taskdef,
            node=None,
        ))
        self.job = job
        self.pod = pod


class KubernetesProvider(ClusterProvider):
    def __init__(self, args = { }):
        super().__init__('kubernetes', args)

        # hacky way to check if we're running within a pod
        if ENV_TASK_CLUSTER in os.environ:
            config.load_incluster_config()
        else:
            config.load_kube_config()

        configuration = client.Configuration()
        self.batch = client.BatchV1Api(kubernetes.client.ApiClient(configuration))
        self.core = client.CoreV1Api(kubernetes.client.ApiClient(configuration))


    def spawn(self, taskdef: TaskDefinition, timeout=30) -> KubernetesTask:
        # container definition
        container = client.V1Container(
            name  = taskdef.id,
            image = taskdef.image, 
            env   = self.create_env(taskdef),
            ports = [ client.V1ContainerPort(container_port=1337) ],
            image_pull_policy='Always',
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
                    metadata=client.V1ObjectMeta(
                        name=taskdef.id,
                    ),
                    spec=client.V1PodSpec(
                        hostname=taskdef.id,
                        containers=[ container ], 
                        restart_policy='Never'
                    ),
                ),
            ),
        )

        # create job
        job = self.batch.create_namespaced_job(taskdef.namespace, jobdef)
        while True:
            pod = self.get_task_pod(taskdef)
            if pod and pod.status.phase != 'Pending':
                break
            timeout -= 1
            if timeout == 0:
                raise TimeoutError(f'Could not find put for {taskdef.id}')
            time.sleep(1)

        # wrap & return task
        print('~~ Spawned kubenetes pod with name', pod.metadata.name)
        return KubernetesTask(self, taskdef, job, pod)


    def destroy(self, task_id):
        raise NotImplementedError()


    def get_task_pod(self, taskdef):
        res = self.core.list_namespaced_pod(
            namespace=taskdef.namespace,
            label_selector=f'job-name={taskdef.id}', 
        )
        return res.items[0] if len(res.items) > 0 else None


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


    def create_env(self, taskdef: TaskDefinition):
        env = super().create_env(taskdef)
        env_list = [ ]
        for name, value in env.items():
            env_list.append(client.V1EnvVar(name, value))
        return env_list

    def destroy_all(self) -> None:
        raise NotImplementedError()

    def destroy_children(self, parent_id: str) -> list:
        raise NotImplementedError()