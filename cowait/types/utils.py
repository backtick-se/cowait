import inspect
from .type import Type
from .simple import Any
from .dict import Dict
from .mapping import convert_type


def convert_type_annotation(annot: object) -> Type:
    """ Converts a type annotation to a cowait type """
    if annot == inspect._empty:
        # an empty type signature defaults to the Any type.
        return Any()
    else:
        return convert_type(annot)


def get_return_type(task) -> Type:
    """ Gets the return type of a Task or task instance. """
    sig = inspect.signature(task.run)
    return convert_type_annotation(sig.return_annotation)


def get_input_types(task) -> Type:
    """
    Gets the input types for a Task or task instance.
    Returns a Dict, mapping parameter names to cowait types.
    """
    sig = inspect.signature(task.run)
    return Dict({
        key: convert_type_annotation(parameter.annotation)
        for key, parameter in sig.parameters.items()
        if parameter.kind == inspect._POSITIONAL_OR_KEYWORD
    })
