import inspect
from .type import Type
from .simple import Any
from .list import List
from .dict import Dict
from .mapping import get_type, convert_type


def convert_type_annotation(annot: object) -> Type:
    """ Converts a type annotation to a cowait type """
    if annot == inspect._empty:
        # an empty type signature defaults to the Any type.
        return Any()

    return convert_type(annot)


def get_parameter_defaults(func: callable) -> dict:
    """ Returns a dict of default parameter values function """
    sig = inspect.signature(func)
    return {
        key: parameter.default
        for key, parameter in sig.parameters.items()
        if parameter.default != inspect._empty
    }


def get_return_type(func: callable) -> Type:
    """ Gets the return type of a function. """
    sig = inspect.signature(func)
    return convert_type_annotation(sig.return_annotation)


def get_parameter_types(func: callable) -> Type:
    """
    Gets the parameter types for a function.
    Returns a Dict, mapping parameter names to cowait types.
    """
    sig = inspect.signature(func)
    return Dict({
        key: convert_type_annotation(parameter.annotation)
        for key, parameter in sig.parameters.items()
        if parameter.kind == inspect._POSITIONAL_OR_KEYWORD
    })


def type_from_description(desc: any) -> Type:
    if isinstance(desc, dict):
        return Dict({
            key: type_from_description(typedesc)
            for key, typedesc in desc.items()
        })
    elif isinstance(desc, list):
        if len(desc) == 0:
            return List()
        elif len(desc) == 1:
            list_type = type_from_description(desc[0])
            return List(list_type)
        else:
            raise TypeError('List typedef should contain a single item')
    elif isinstance(desc, str):
        # it should be a type name!
        return get_type(desc)()
    else:
        raise TypeError('Invalid type description')


def typed_arguments(func: callable, args: dict) -> dict:
    """
    Checks argument types against function signature and deserializes using cowait types.
    """
    # validate args
    parameter_types = get_parameter_types(func)
    parameter_types.validate(args, 'Arguments')

    # deeserialize args
    return parameter_types.deserialize(args)


def typed_return(func: callable, result: object) -> object:
    """
    Type checks and serializes a return value using cowait types.
    """
    result_type = get_return_type(func)
    if isinstance(result_type, Any):
        result_type = guess_type(result)

    # serialize & validate
    data = result_type.serialize(result)
    result_type.validate(data, 'Return')
    return data, result_type


async def typed_call(func: callable, args: dict) -> object:
    """ Performs a type-checked function call. """
    args = {
        **get_parameter_defaults(func),
        **args,
    }
    args = typed_arguments(func, args)
    result = func(**args)
    return typed_return(func, result)


async def typed_async_call(func: callable, args: dict) -> object:
    """ Performs a type-checked asynchronous function call. """
    args = {
        **get_parameter_defaults(func),
        **args,
    }
    targs = typed_arguments(func, args)
    result = await func(**targs)
    return typed_return(func, result)


def guess_type(obj: object) -> Type:
    """
    Attempts to guess the cowait type of an object by checking if
    its type has a registered cowait type mapping.

    Raises a TypeError if obj is not a valid cowait type.
    """
    return convert_type(type(obj))


def validate_type(obj: object, shape: Type = None) -> bool:
    """
    Validates the type of an object. If no type is provided, it will
    be inferred from the value. Returns true if the object is a valid
    cowait type.
    """
    if shape is None:
        shape = guess_type(obj)

    try:
        shape.validate(obj)
        return True
    except ValueError:
        return False


def serialize(obj: object, shape: Type = None) -> object:
    """ Best-effort serialization of an object """
    if shape is None:
        shape = guess_type(obj)

    return shape.serialize(obj)


def deserialize(obj: any, typedesc: any) -> object:
    type = type_from_description(typedesc)
    return type.deserialize(obj)
