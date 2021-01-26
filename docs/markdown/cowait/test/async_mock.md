Module cowait.test.async_mock
=============================

Classes
-------

`AsyncMock(*args, **kw)`
:   MagicMock is a subclass of Mock with default implementations
    of most of the magic methods. You can use MagicMock without having to
    configure the magic methods yourself.
    
    If you use the `spec` or `spec_set` arguments then *only* magic
    methods that exist in the spec will be created.
    
    Attributes and the return value of a `MagicMock` will also be `MagicMocks`.

    ### Ancestors (in MRO)

    * unittest.mock.MagicMock
    * unittest.mock.MagicMixin
    * unittest.mock.Mock
    * unittest.mock.CallableMixin
    * unittest.mock.NonCallableMock
    * unittest.mock.Base