Module cowait.tasks.shell.shell
===============================

Functions
---------

    
`print_stream(stream, name: str, filter: <built-in function callable>) ‑> NoneType`
:   

Classes
-------

`ShellTask(**inputs)`
:   Creates a new instance of the task. Pass inputs as keyword arguments.

    ### Ancestors (in MRO)

    * cowait.tasks.task.Task

    ### Descendants

    * cowait.tasks.dask.scheduler.DaskScheduler
    * cowait.tasks.dask.worker.DaskWorker

    ### Methods

    `filter_stderr(self, line: str) ‑> bool`
    :

    `filter_stdout(self, line: str) ‑> bool`
    :

    `run(self, command: str, env: dict = {}) ‑> <cowait.types.dict.Dict object at 0x110ee9e10>`
    :