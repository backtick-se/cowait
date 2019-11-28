import os
import time
import kubernetes
from kubernetes import client, config, watch
from pipeline.tasks import Task, TaskContext, TaskDefinition
from .const import ENV_TASK_CLUSTER
from .cluster import ClusterProvider

# for now, all tasks live in the same namespace.
NAMESPACE = 'default'
LABEL_TASK_ID = 'pipeline/task'
LABEL_PARENT_ID = 'pipeline/parent'


class KubernetesTask(Task):
    def __init__(
        self,
        cluster: ClusterProvider,
        taskdef: TaskDefinition,
        job,
        pod,
    ):
        super().__init__(TaskContext(
            cluster=cluster,
            taskdef=taskdef,
            node=None,
        ))
        self.job = job
        self.pod = pod


class KubernetesProvider(ClusterProvider):
    def __init__(self, args={}):
        super().__init__('kubernetes', args)

        # hacky way to check if we're running within a pod
        if ENV_TASK_CLUSTER in os.environ:
            config.load_incluster_config()
        else:
            config.load_kube_config()

        configuration = client.Configuration()
        self.batch = client.BatchV1Api(
            kubernetes.client.ApiClient(configuration))
        self.core = client.CoreV1Api(
            kubernetes.client.ApiClient(configuration))

    def spawn(self, taskdef: TaskDefinition, timeout=30) -> KubernetesTask:
        # container definition
        container = client.V1Container(
            name=taskdef.id,
            image=taskdef.image,
            env=self.create_env(taskdef),
            ports=[client.V1ContainerPort(container_port=1337)],
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
                        labels={
                            LABEL_TASK_ID: taskdef.id,
                            LABEL_PARENT_ID: taskdef.parent,
                        },
                    ),
                    spec=client.V1PodSpec(
                        hostname=taskdef.id,
                        containers=[container],
                        restart_policy='Never'
                    ),
                ),
            ),
        )

        # create job
        job = self.batch.create_namespaced_job(taskdef.namespace, jobdef)
        while True:
            pod = self.get_task_pod(taskdef.id)
            if pod and pod.status.phase != 'Pending':
                break
            timeout -= 1
            if timeout == 0:
                raise TimeoutError(f'Could not find pod for {taskdef.id}')
            time.sleep(1)

        # wrap & return task
        print('~~ created kubenetes pod with name', pod.metadata.name)
        return KubernetesTask(self, taskdef, job, pod)

    def destroy(self, task_id):
        self.core.delete_collection_namespaced_pod(
            namespace=NAMESPACE,
            label_selector=f'{LABEL_TASK_ID}={task_id}',
        )
        return task_id

    def get_task_pod(self, task_id):
        res = self.core.list_namespaced_pod(
            namespace=NAMESPACE,
            label_selector=f'{LABEL_TASK_ID}={task_id}',
        )
        return res.items[0] if len(res.items) > 0 else None

    def get_task_child_pods(self, task_id: str):
        res = self.core.list_namespaced_pod(
            namespace=NAMESPACE,
            label_selector=f'{LABEL_PARENT_ID}={task_id}',
        )
        return res.items

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
        try:
            w = watch.Watch()
            return w.stream(
                self.core.read_namespaced_pod_log,
                name=task.pod.metadata.name,
                namespace=task.pod.metadata.namespace,
            )
        except Exception:
            self.logs(task)

    def create_env(self, taskdef: TaskDefinition):
        env = super().create_env(taskdef)
        env_list = []
        for name, value in env.items():
            env_list.append(client.V1EnvVar(name, value))
        return env_list

    def destroy_all(self, task_id) -> None:
        def kill_family(task_id):
            kills = []
            children = self.get_task_child_pods(task_id)
            for child in children.items:
                child_id = child.metadata.labels[LABEL_TASK_ID]
                kills += kill_family(child_id)

            self.destroy(task_id)
            kills.append(task_id)

        return kill_family(task_id)

    def destroy_children(self, parent_id: str) -> list:
        children = self.core.list_namespaced_pod(
            namespace=NAMESPACE,
            label_selector=f'{LABEL_PARENT_ID}={parent_id}',
        )

        self.core.delete_collection_namespaced_pod(
            namespace=NAMESPACE,
            label_selector=f'{LABEL_PARENT_ID}={parent_id}',
        )

        # return killed child ids
        return [
            child.metadata.labels[LABEL_TASK_ID]
            for child in children.items
        ]
