Module cowait.tasks.task
========================

Classes
-------

`Task(**inputs)`
:   Creates a new instance of the task. Pass inputs as keyword arguments.

    ### Descendants

    * cowait.tasks.agent.agent.Agent
    * cowait.tasks.container.container_task.ContainerTask
    * cowait.tasks.dask.cluster.DaskCluster
    * cowait.tasks.schedule.schedule.ScheduleTask
    * cowait.tasks.shell.shell.ShellTask
    * cowait.test.tasks.rpc_child.RpcChild
    * cowait.test.tasks.rpc_parent.RpcParent
    * cowait.test.tasks.utility.UtilityTask
    * cowait.test.test_task.PytestTask
    * cowait.test.utils.double_task_def.TaskOne
    * cowait.test.utils.double_task_def.TaskTwo

    ### Static methods

    `get_current() ‑> cowait.tasks.task.Task`
    :

    `set_current(task: Task)`
    :

    ### Instance variables

    `id: str`
    :

    `image: str`
    :

    `meta: dict`
    :

    ### Methods

    `after(self, inputs: dict) ‑> Any`
    :

    `before(self, inputs: dict) ‑> dict`
    :

    `init(self)`
    :

    `run(self, **inputs: dict) ‑> Any`
    :

    `spawn(self, name: str, id: str = None, image: str = None, ports: dict = {}, routes: dict = {}, inputs: dict = {}, meta: dict = {}, env: dict = {}, volumes: dict = {}, cpu: str = None, cpu_limit: str = None, memory: str = None, memory_limit: str = None, affinity: str = None, owner: str = '', **kwargs: dict) ‑> cowait.tasks.task.Task`
    :   Spawn a subtask.
        
        Arguments:
            name (str): Task name
            image (str): Task image. Defaults to the current task image.
            kwargs (dict): Input arguments

    `stop(self) ‑> NoneType`
    :   Abort task execution.