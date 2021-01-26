Module cowait.types.numpy
=========================

Classes
-------

`NumpyArray()`
:   Abstract base class for all Cowait types.

    ### Ancestors (in MRO)

    * cowait.types.type.Type
    * abc.ABC

    ### Class variables

    `name: str`
    :

`NumpyBool()`
:   Boolean

    ### Ancestors (in MRO)

    * cowait.types.simple.Bool
    * cowait.types.type.Type
    * abc.ABC

    ### Class variables

    `name: str`
    :

`NumpyFloat()`
:   Floating point, or anything that can be cast to a float

    ### Ancestors (in MRO)

    * cowait.types.simple.Float
    * cowait.types.type.Type
    * abc.ABC

    ### Class variables

    `name: str`
    :

`NumpyInt()`
:   Integer, or anything that can be cast to an integer

    ### Ancestors (in MRO)

    * cowait.types.simple.Int
    * cowait.types.type.Type
    * abc.ABC

    ### Class variables

    `name: str`
    :