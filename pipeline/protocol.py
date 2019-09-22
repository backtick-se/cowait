from typing import Any
from pipeline.tasks.status import *


def msg(type, **fields):
    return {
        'type': type,
        **fields,
    }

def InitMsg(taskdef) -> None:
    """
    Send a task initialization message.

    Arguments:
        taskdef (TaskDefinition): New task definition
    """
    return msg('init', task=taskdef.serialize())


def RunMsg() -> None:
    """ Send status update: Running """
    return msg('status', status=WORK)


def StopMsg(id=None) -> None:
    """ Send status update: Stopped """
    return [
        msg('status', status=STOP, id=id),
        msg('return', result={}, id=id),
    ]


def DoneMsg(result: Any) -> None:
    """ 
    Send status update: Done, and return a result.

    Arguments:
        result (any): Any json-serializable data to return to the upstream task.
    """
    return [
        msg('status', status=DONE),
        msg('return', result=result),
    ]


def FailMsg(error: str) -> None:
    """
    Send an error.

    Arguments:
        error (str): Error message
    """
    return [
        msg('status', status=FAIL),
        msg('fail',   error=error),
    ]


def LogMsg(file: str, data: str) -> None:
    """
    Send captured log output.

    Arguments:
        file (str): Capture source (stdout/stderr)
        data (str): Captured output data
    """
    return msg('log', file=file, data=data)
