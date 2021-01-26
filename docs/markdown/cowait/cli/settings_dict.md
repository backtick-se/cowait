Module cowait.cli.settings_dict
===============================

Functions
---------

    
`split_key(key)`
:   

Classes
-------

`SettingsDict(*, path: str = None, data: dict = None, parent: SettingsDict = None)`
:   

    ### Descendants

    * cowait.cli.config.Config

    ### Methods

    `coalesce(self, key: str, value: <built-in function any>, default: <built-in function any>) ‑> <built-in function any>`
    :

    `delete(self, key: str) ‑> NoneType`
    :

    `get(self, key: str, default: <built-in function any> = None, required: bool = True) ‑> <built-in function any>`
    :

    `has(self, key: str) ‑> bool`
    :

    `override(self, key: str, value: <built-in function any>) ‑> <built-in function any>`
    :

    `pack_data(self, data)`
    :

    `read(self, path)`
    :

    `set(self, key: str, value: <built-in function any>) ‑> <built-in function any>`
    :

    `unpack_data(self, data)`
    :

    `write(self, path)`
    :