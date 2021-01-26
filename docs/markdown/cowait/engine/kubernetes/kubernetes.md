Module cowait.engine.kubernetes.kubernetes
==========================================

Classes
-------

`KubernetesProvider(args={})`
:   

    ### Ancestors (in MRO)

    * cowait.engine.cluster.ClusterProvider
    * cowait.utils.emitter.EventEmitter

    ### Instance variables

    `domain`
    :

    `namespace`
    :

    `service_account`
    :

    `timeout`
    :

    ### Methods

    `destroy_all(self) ‑> list`
    :

    `destroy_children(self, parent_id: str) ‑> list`
    :

    `find_agent(self)`
    :

    `get_pull_secrets(self)`
    :

    `get_task_child_pods(self, task_id: str)`
    :

    `get_task_pod(self, task_id)`
    :

    `kill(self, task_id)`
    :

    `list_all(self) ‑> list`
    :

    `wait_until_ready(self, task_id: str, poll_interval: float = 0.5)`
    :