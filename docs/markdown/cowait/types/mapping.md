Module cowait.types.mapping
===========================

Functions
---------

    
`TypeAlias(*aliases: ClassVar)`
:   Registers a type alias for the decorated type

    
`convert_type(type: <built-in function any>) ‑> cowait.types.type.Type`
:   Converts a python type to a cowait type

    
`get_type(name: str) ‑> cowait.types.type.Type`
:   

    
`instantiate_type(TypeClass: ClassVar) ‑> object`
:   Attempts to automatically instantiate a cowait type class

    
`is_cowait_type(type: <built-in function any>) ‑> bool`
:   Checks if a type is a valid cowait type

    
`param_without_default(p: inspect.Parameter) ‑> bool`
:   Checks if a function parameter has no default value

    
`register_type(from_type: ClassVar, to_type: cowait.types.type.Type) ‑> NoneType`
:   Registers a type alias for the given from_type