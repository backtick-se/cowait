Module cowait.cli.commands.run
==============================

Functions
---------

    
`run(config: cowait.cli.config.Config, task: str, *, name: str = None, inputs: dict = {}, env: dict = {}, ports: dict = {}, routes: dict = {}, build: bool = False, upstream: str = None, detach: bool = False, cpu: str = None, cpu_limit: str = None, memory: str = None, memory_limit: str = None, raw: bool = False, quiet: bool = False, affinity: str = None, cluster_name: str = None)`
:   

Classes
-------

`RunLogger(raw: bool = False, quiet: bool = False, time: bool = True)`
:   

    ### Ancestors (in MRO)

    * cowait.cli.logger.Logger

    ### Instance variables

    `newline_indent`
    :

    ### Methods

    `handle(self, msg)`
    :

    `header(self, title: str = None)`
    :

    `on_fail(self, id: str, error: str, ts: str = None, **msg)`
    :

    `on_init(self, task: dict, version: str, ts: str = None, **msg)`
    :

    `on_log(self, id: str, file: str, data: str, ts: str = None, **msg)`
    :

    `on_return(self, id: str, result: <built-in function any>, ts: str = None, **msg)`
    :

    `on_status(self, id: str, status: str, ts: str = None, **msg)`
    :

    `print(self, *args)`
    :

    `print_id(self, id, ts=None, short=True, pad=True)`
    :

    `print_info(self, taskdef, cluster)`
    :