Module cowait.tasks.container.container_task
============================================

Classes
-------

`ContainerTask(**inputs)`
:   Creates a new instance of the task. Pass inputs as keyword arguments.

    ### Ancestors (in MRO)

    * cowait.tasks.task.Task

    ### Methods

    `run(self, name: str, image: str, env: dict = {}, routes: dict = {}, ports: dict = {}, cpu: <built-in function any> = 0, memory: <built-in function any> = 0, **inputs)`
    :

    `watch(self, task)`
    :