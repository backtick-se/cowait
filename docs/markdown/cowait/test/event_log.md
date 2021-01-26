Module cowait.test.event_log
============================

Functions
---------

    
`dict_match(search: dict, item: dict) ‑> bool`
:   

Classes
-------

`EventLog(*args, **kwargs)`
:   EventList is used to organize and query task event output.

    ### Ancestors (in MRO)

    * builtins.list

    ### Methods

    `collect(self, stream: <built-in function iter>)`
    :   Collects all the output events from a task.

    `count(self, **search: dict) ‑> int`
    :   Return number of occurrences of value.

    `extract(self, key: str) ‑> list`
    :

    `has(self, **search: dict) ‑> bool`
    :   Checks if a event of a certain type has been captured with fields matching the provided
        regex dict. Each value in the search dict is matched against the event value at the
        corresponding key.

    `match(self, **search: dict) ‑> list`
    :   Returns all events with fields matching the provided regex dict.
        Each value in the search dict is matched against the event value at the corresponding key.

    `match_one(self, **search: dict) ‑> dict`
    :   Returns the first event fields matching the provided regex dict.
        Each value in the search dict is matched against the event value at the corresponding key.

    `unique(self, key) ‑> set`
    :