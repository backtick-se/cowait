Module cowait.cli.context
=========================

Classes
-------

`Context(root_path: str, *, path: str, parent: cowait.cli.config.Config)`
:   

    ### Ancestors (in MRO)

    * cowait.cli.config.Config
    * cowait.cli.settings_dict.SettingsDict

    ### Static methods

    `exists(path: str = None)`
    :

    `open(config: cowait.cli.config.Config, path: str = None)`
    :

    ### Instance variables

    `base`
    :

    `environment`
    :

    `image`
    :

    `workdir: str`
    :

    ### Methods

    `file(self, file_name: str) ‑> str`
    :   Find a file within the task context and return its full path

    `file_rel(self, file_name: str) ‑> str`
    :   Find a file within the task context and return its relative path

    `includes(self, path: str) ‑> bool`
    :   Checks if the path is included in the context

    `pack_data(self, data: dict) ‑> dict`
    :

    `relpath(self, context_path: str)`
    :   Returns a path relative to the context root

    `unpack_data(self, data: dict) ‑> dict`
    :

    `write(self, path: str = None) ‑> NoneType`
    :