Module cowait.tasks.components.rpc
==================================

Functions
---------

    
`get_rpc_methods(object)`
:   Returns a dict of functions marked with @rpc on the given object

    
`is_rpc_method(object)`
:   Returns true if the given object is a method marked with @rpc

    
`rpc(f)`
:   Decorator for marking RPC methods

Classes
-------

`RpcComponent(task)`
:   

    ### Methods

    `call(self, method, args)`
    :

    `get_method(self, method: str) ‑> <built-in function callable>`
    :

    `http_rpc_handler(self, req)`
    :

    `on_rpc(self, conn, method, args, nonce)`
    :

`RpcError(*args, **kwargs)`
:   Unspecified run-time error.

    ### Ancestors (in MRO)

    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException