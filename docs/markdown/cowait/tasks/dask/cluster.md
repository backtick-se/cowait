Module cowait.tasks.dask.cluster
================================

Classes
-------

`DaskCluster(**inputs)`
:   Creates a new instance of the task. Pass inputs as keyword arguments.

    ### Ancestors (in MRO)

    * cowait.tasks.task.Task

    ### Methods

    `add_workers(self, count)`
    :

    `after(self, inputs: dict)`
    :

    `before(self, inputs: dict) ‑> dict`
    :

    `create_cluster(self, workers=1) ‑> NoneType`
    :

    `get_client(self) ‑> distributed.client.Client`
    :   Returns a Dask client for this cluster

    `get_scheduler_uri(self) ‑> str`
    :

    `get_workers(self)`
    :

    `init(self)`
    :

    `on_log(self, id, file, data, **msg) ‑> NoneType`
    :

    `remove_workers(self, count)`
    :

    `run(self, workers: int = 5)`
    :

    `scale(self, workers: int)`
    :

    `teardown(self) ‑> NoneType`
    :

    `wait_for_nodes(self)`
    :