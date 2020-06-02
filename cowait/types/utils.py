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
        if '@' in desc:
            CustomType = get_type(desc['@'])
            del desc['@']
            return CustomType(**desc)
        else:
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
