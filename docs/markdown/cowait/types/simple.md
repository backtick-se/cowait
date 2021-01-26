Module cowait.types.simple
==========================

Classes
-------

`Any()`
:   Any type. Disables typechecking.

    ### Ancestors (in MRO)

    * cowait.types.type.Type
    * abc.ABC

    ### Class variables

    `name: str`
    :

`Bool()`
:   Boolean

    ### Ancestors (in MRO)

    * cowait.types.type.Type
    * abc.ABC

    ### Descendants

    * cowait.types.numpy.NumpyBool

    ### Class variables

    `name: str`
    :

`DateTime()`
:   Python datetime object serialized as an ISO8601 string

    ### Ancestors (in MRO)

    * cowait.types.type.Type
    * abc.ABC

    ### Class variables

    `name: str`
    :

`Float()`
:   Floating point, or anything that can be cast to a float

    ### Ancestors (in MRO)

    * cowait.types.type.Type
    * abc.ABC

    ### Descendants

    * cowait.types.numpy.NumpyFloat

    ### Class variables

    `name: str`
    :

`Int()`
:   Integer, or anything that can be cast to an integer

    ### Ancestors (in MRO)

    * cowait.types.type.Type
    * abc.ABC

    ### Descendants

    * cowait.types.numpy.NumpyInt

    ### Class variables

    `name: str`
    :

`String()`
:   String

    ### Ancestors (in MRO)

    * cowait.types.type.Type
    * abc.ABC

    ### Class variables

    `name: str`
    :

`Void()`
:   Abstract base class for all Cowait types.

    ### Ancestors (in MRO)

    * cowait.types.type.Type
    * abc.ABC

    ### Class variables

    `name: str`
    :