Module cowait.cli.config
========================

Functions
---------

    
`get_global_config_path()`
:   

Classes
-------

`Config(*, path: str = None, data: dict = None, parent: Config = None)`
:   

    ### Ancestors (in MRO)

    * cowait.cli.settings_dict.SettingsDict

    ### Descendants

    * cowait.cli.context.Context

    ### Static methods

    `get_default() ‑> cowait.cli.config.Config`
    :

    `get_global() ‑> cowait.cli.config.Config`
    :

    `get_local(path: str = None) ‑> cowait.cli.config.Config`
    :

    ### Instance variables

    `clusters: list`
    :

    `default_cluster: str`
    :

    ### Methods

    `get_cluster(self, cluster_name: str = None)`
    :

    `write(self) ‑> NoneType`
    :