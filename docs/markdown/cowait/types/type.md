Module cowait.types.type
========================

Classes
-------

`Type()`
:   Abstract base class for all Cowait types.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * cowait.tasks.dask.types.DaskClientType
    * cowait.types.custom.CustomType
    * cowait.types.dict.Dict
    * cowait.types.fs.FileType
    * cowait.types.list.List
    * cowait.types.numpy.NumpyArray
    * cowait.types.simple.Any
    * cowait.types.simple.Bool
    * cowait.types.simple.DateTime
    * cowait.types.simple.Float
    * cowait.types.simple.Int
    * cowait.types.simple.String
    * cowait.types.simple.Void

    ### Class variables

    `name: str`
    :

    ### Methods

    `describe(self) ‑> <built-in function any>`
    :   Creates a JSON-serializable type description for this type

    `deserialize(self, value: any) ‑> cowait.types.type.Type`
    :   Deserializes a JSON representation of a value

    `serialize(self, value: Type) ‑> object`
    :   Returns a JSON-serializable representation of the value

    `validate(self, value: any, name: str) ‑> NoneType`
    :   Validates a value as this type. Raises ValueError if invalid