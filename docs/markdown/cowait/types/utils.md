Module cowait.types.utils
=========================

Functions
---------

    
`convert_type_annotation(annot: object) ‑> cowait.types.type.Type`
:   Converts a type annotation to a cowait type

    
`deserialize(obj: <built-in function any>, typedesc: <built-in function any>) ‑> object`
:   

    
`get_parameter_defaults(func: <built-in function callable>) ‑> dict`
:   Returns a dict of default parameter values function

    
`get_parameter_types(func: <built-in function callable>) ‑> cowait.types.type.Type`
:   Gets the parameter types for a function.
    Returns a Dict, mapping parameter names to cowait types.

    
`get_return_type(func: <built-in function callable>) ‑> cowait.types.type.Type`
:   Gets the return type of a function.

    
`guess_type(obj: object) ‑> cowait.types.type.Type`
:   Attempts to guess the cowait type of an object by checking if
    its type has a registered cowait type mapping.
    
    Raises a TypeError if obj is not a valid cowait type.

    
`serialize(obj: object, shape: cowait.types.type.Type = None) ‑> object`
:   Best-effort serialization of an object

    
`type_from_description(desc: <built-in function any>) ‑> cowait.types.type.Type`
:   

    
`typed_arguments(func: <built-in function callable>, args: dict) ‑> dict`
:   Checks argument types against function signature and deserializes using cowait types.

    
`typed_async_call(func: <built-in function callable>, args: dict) ‑> object`
:   Performs a type-checked asynchronous function call.

    
`typed_call(func: <built-in function callable>, args: dict) ‑> object`
:   Performs a type-checked function call.

    
`typed_return(func: <built-in function callable>, result: object) ‑> object`
:   Type checks and serializes a return value using cowait types.

    
`validate_type(obj: object, shape: cowait.types.type.Type = None) ‑> bool`
:   Validates the type of an object. If no type is provided, it will
    be inferred from the value. Returns true if the object is a valid
    cowait type.