Module cowait.network.rpc_client
================================

Classes
-------

`RpcCall(method, args, nonce)`
:   Represents the result of an asynchronous computation.
    
    Initializes the future. Should not be called by clients.

    ### Ancestors (in MRO)

    * concurrent.futures._base.Future

`RpcClient(ws)`
:   

    ### Methods

    `call(self, method, args)`
    :

    `cancel_all(self)`
    :

    `intercept_event(self, type, **msg)`
    :