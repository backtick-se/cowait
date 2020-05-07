import inspect
import cowait.types


def is_cowait_type(type):
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
    else:
        return isinstance(type, cowait.types.Type)


def convert_type_annotation(annot):
    """ Converts a type annotation to a cowait type """
    if annot == inspect._empty:
        return cowait.types.Any()
    else:
        return convert_type(annot)


def convert_type(type):
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
    else:
        raise TypeError('Expected a valid cowait type')


def get_return_type(task):
    """ Gets the return type of a Task or task instance. """
    sig = inspect.signature(task.run)
    return convert_type_annotation(sig.return_annotation)


def get_input_types(task):
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
