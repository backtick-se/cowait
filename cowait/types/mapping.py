import inspect
from functools import reduce
from typing import ClassVar
from .type import Type


_type_mapping = {}
_name_mapping = {}


def register_type(from_type: ClassVar, to_type: Type) -> None:
    """ Registers a type alias for the given from_type """
    global _name_mapping
    global _type_mapping
    if to_type.name is None:
        to_type.name = f'{to_type.__module__}.{to_type.__name__}'
    _name_mapping[to_type.name] = to_type
    _type_mapping[from_type] = to_type
    _name_mapping[f'{to_type.__module__}.{to_type.__name__}'] = to_type


def get_type(name: str) -> Type:
    global _name_mapping
    if name in _name_mapping:
        return _name_mapping[name]
    raise TypeError(f'Unknown type {name}')


def TypeAlias(*aliases: ClassVar):
    """ Registers a type alias for the decorated type """
    def register_alias(cls: ClassVar):
        if not is_cowait_type(cls):
            raise TypeError(f'{cls} must be a valid cowait type')

        for alias in aliases:
            register_type(alias, cls)

        return cls

    return register_alias


def is_cowait_type(type: any) -> bool:
    """ Checks if a type is a valid cowait type """
    global _type_mapping

    if isinstance(type, Type):
        return True
    elif type in _type_mapping:
        # type can be considered a cowait type if we have
        # a registered mapping for it.
        return True
    elif inspect.isclass(type) and issubclass(type, Type):
        # classes that can be instantiated to type objects
        # are also considered valid.
        return True

    return False


def convert_type(type: any) -> Type:
    """ Converts a python type to a cowait type """
    global _type_mapping

    if isinstance(type, Type):
        # if passed a valid Cowait type instance, simply return it
        return type

    elif type in _type_mapping:
        # check if we have a registered mapping for this type.
        # if so, instantiate that the mapped type.
        mapped_type = _type_mapping[type]
        return instantiate_type(mapped_type)

    elif inspect.isclass(type) and issubclass(type, Type):
        # if passed a valid Cowait type class, attempt to instantiate it
        return instantiate_type(type)

    else:
        raise TypeError(f'Expected {type} to be a valid cowait type')


def param_without_default(p: inspect.Parameter) -> bool:
    """ Checks if a function parameter has no default value """

    # self parameter does not need a default.
    if p.name == 'self':
        return False

    # variable arguments do not need defaults
    if p.kind == inspect._VAR_KEYWORD or \
       p.kind == inspect._VAR_POSITIONAL:
        return False

    return p.default == inspect.Parameter.empty


def instantiate_type(TypeClass: ClassVar) -> object:
    """ Attempts to automatically instantiate a cowait type class """

    # count number of __init__ parameters without a default value
    sig = inspect.signature(TypeClass.__init__)

    non_default_params = reduce(
        lambda c, p: c+1 if param_without_default(p) else c,
        sig.parameters.values(),
        0,
    )

    # can't auto instantiate if there are non-default parameters
    if (non_default_params > 0):
        raise TypeError(f'{TypeClass.__name__} has non-default parameters '
                        f'and cant be automatically instantiated')

    instance = TypeClass()
    return instance
