Module cowait.engine.docker.docker
==================================

Classes
-------

`DockerProvider(args={})`
:   

    ### Ancestors (in MRO)

    * cowait.engine.cluster.ClusterProvider
    * cowait.utils.emitter.EventEmitter

    ### Instance variables

    `network`
    :

    ### Methods

    `create_ports(self, taskdef)`
    :

    `destroy(self, task_id)`
    :   Destroy a specific task id and all its descendants

    `destroy_all(self) ‑> NoneType`
    :   Destroys all running tasks

    `destroy_children(self, parent_id: str) ‑> list`
    :   Destroy all child tasks of a given task id

    `ensure_network(self)`
    :

    `find_agent(self)`
    :

    `find_child_containers(self, parent_id: str) ‑> list`
    :   Finds all child containers of a given task id

    `list_all(self) ‑> list`
    :   Returns a list of all running tasks

    `logs(self, task: cowait.engine.docker.task.DockerTask)`
    :   Stream task logs

    `wait(self, task: cowait.engine.docker.task.DockerTask) ‑> bool`
    :   Wait for a task to finish. Returns True on clean exit