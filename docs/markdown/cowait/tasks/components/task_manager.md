Module cowait.tasks.components.task_manager
===========================================

Classes
-------

`TaskManager(task)`
:   Keeps track of the state of subtasks

    ### Ancestors (in MRO)

    * builtins.dict

    ### Methods

    `emit_child_error(self, id, error, conn=None)`
    :

    `on_child_close(self, conn, **msg: dict) ‑> NoneType`
    :

    `on_child_fail(self, conn, id: str, error: str, **msg: dict)`
    :

    `on_child_init(self, conn, id: str, task: dict, version: str, **msg: dict)`
    :

    `on_child_return(self, conn, id: str, result: Any, result_type: <built-in function any>, **msg: dict)`
    :

    `on_child_status(self, conn, id: str, status: str, **msg: dict)`
    :

    `set_init_timeout(self, task, timeout)`
    :

    `watch(self, task, timeout=30)`
    :