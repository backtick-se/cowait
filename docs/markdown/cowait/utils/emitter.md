Module cowait.utils.emitter
===========================

Classes
-------

`EventEmitter()`
:   

    ### Descendants

    * cowait.engine.cluster.ClusterProvider
    * cowait.network.client.Client
    * cowait.network.server.Server
    * cowait.tasks.agent.subscriptions.Subscriptions

    ### Methods

    `emit(self, type: str, **kwargs: dict) ‑> NoneType`
    :

    `emit_sync(self, type: str, **kwargs: dict) ‑> NoneType`
    :

    `off(self, type: str, callback: <built-in function callable>) ‑> NoneType`
    :

    `on(self, type: str, callback: <built-in function callable>) ‑> <built-in function callable>`
    :