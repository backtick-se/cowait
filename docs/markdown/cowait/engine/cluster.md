Module cowait.engine.cluster
============================

Classes
-------

`ClusterProvider(type, args={})`
:   

    ### Ancestors (in MRO)

    * cowait.utils.emitter.EventEmitter

    ### Descendants

    * cowait.engine.api.ApiProvider
    * cowait.engine.docker.docker.DockerProvider
    * cowait.engine.kubernetes.kubernetes.KubernetesProvider

    ### Methods

    `create_env(self, taskdef: TaskDefinition) ‑> dict`
    :   Create a container environment dict from a task definition.
        
        Arguments:
            taskdef (TaskDefinition): Task definition
        
        Returns:
            env (dict): Environment variable dict

    `destroy(self, task_id: str) ‑> NoneType`
    :   Destroy a task

    `destroy_all(self) ‑> NoneType`
    :

    `destroy_children(self, parent_id: str) ‑> NoneType`
    :

    `find_agent(self)`
    :

    `list_all(self) ‑> list`
    :

    `logs(self, task: RemoteTask) ‑> Iterable[str]`
    :   Stream logs from task

    `serialize(self) ‑> dict`
    :   Serialize ClusterProvider into a dict

    `spawn(self, taskdef: TaskDefinition) ‑> cowait.tasks.remote_task.RemoteTask`
    :   Spawn a task in the cluster

    `wait(self, task: RemoteTask) ‑> bool`
    :   Wait for task to exit. Returns True on clean exit.