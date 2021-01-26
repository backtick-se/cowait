Module cowait.network.auth_middleware
=====================================

Classes
-------

`AuthMiddleware()`
:   

    ### Methods

    `add_token(self, token: str) ‑> NoneType`
    :

    `ban_token(self, token: str) ‑> NoneType`
    :

    `get_token(self) ‑> str`
    :

    `is_public(self, path)`
    :

    `middleware(self, request, handler)`
    :

    `validate_token(self, token: str) ‑> bool`
    :