Module cowait.network.client
============================

Classes
-------

`Client()`
:   

    ### Ancestors (in MRO)

    * cowait.utils.emitter.EventEmitter

    ### Descendants

    * cowait.worker.parent_client.ParentClient

    ### Instance variables

    `connected: bool`
    :

    ### Methods

    `close(self)`
    :

    `connect(self, url: str, token: str, max_retries: int = 5) ‑> NoneType`
    :

    `send(self, msg: dict) ‑> NoneType`
    :