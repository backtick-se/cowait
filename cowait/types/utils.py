import inspect
import cowait.types
from functools import reduce


def is_cowait_type(type: any) -> bool:
    """ Checks if a type is a valid cowait type """
    if type == any:
        return True
    elif type == int:
        return True
    elif type == float:
        return True
    elif type == str:
        return True
    elif type == bool:
        return True
    elif type == dict:
        return True
    elif type == list:
        return True
    elif isinstance(type, cowait.types.Type):
        return True
    elif inspect.isclass(type) and issubclass(type, cowait.types.Type):
        return True
    return False


def convert_type_annotation(annot: object) -> 'cowait.types.Type':
    """ Converts a type annotation to a cowait type """
    if annot == inspect._empty:
        # an empty type signature defaults to the Any type.
        return cowait.types.Any()
    else:
        return convert_type(annot)


def convert_type(type: any) -> 'cowait.types.Type':
    """ Converts a python type to a cowait type """
    if type == any:
        return cowait.types.Any()
    elif type == int:
        return cowait.types.Int()
    elif type == float:
        return cowait.types.Float()
    elif type == str:
        return cowait.types.String()
    elif type == bool:
        return cowait.types.Bool()
    elif type == dict:
        return cowait.types.Dict()
    elif type == list:
        return cowait.types.List()
    elif isinstance(type, cowait.types.Type):
        return type
    elif inspect.isclass(type) and issubclass(type, cowait.types.Type):
        return instantiate_type(type)
    else:
        raise TypeError('Expected a valid cowait type')


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


def instantiate_type(TypeClass) -> object:
    """ Attempts to automatically instantiate a cowait type class """

    # count number of __init__ parameters without a default value
    sig = inspect.signature(TypeClass.__init__)

    non_default_params = reduce(
        lambda c, p: c+1 if param_without_default(p) else c,
        sig.parameters.values(),
        0,
    )

    print(list(sig.parameters.values()))

    # can't auto instantiate if there are non-default parameters
    if (non_default_params > 0):
        raise TypeError(f'{TypeClass.__name__} has non-default parameters '
                        f'and cant be automatically instantiated')

    instance = TypeClass()
    return instance


def get_return_type(task: 'cowait.Task') -> 'cowait.types.Type':
    """ Gets the return type of a Task or task instance. """
    sig = inspect.signature(task.run)
    return convert_type_annotation(sig.return_annotation)


def get_input_types(task: 'cowait.Task') -> 'cowait.types.Type':
    """
    Gets the input types for a Task or task instance.
    Returns a Dict, mapping parameter names to cowait types.
    """
    sig = inspect.signature(task.run)
    return cowait.types.Dict({
        key: convert_type_annotation(parameter.annotation)
        for key, parameter in sig.parameters.items()
        if parameter.kind == inspect._POSITIONAL_OR_KEYWORD
    })
