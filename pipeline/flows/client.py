from abc import ABC, abstractmethod
from typing import Any
from pipeline.tasks.status import *
from pipeline.network import PushSocket, NoopSocket


class FlowClient(object):
    """ Upstream Client """

    def __init__(self, id: str, upstream = None):
        """
        Create a new PushConnector.

        Arguments:
            id (str): Local task id
            parent (str): Parent connection string
        """
        self.id = id
        self.services = [ ]
        self.upstream = NoopSocket() if upstream is None else PushSocket(upstream)


    def attach(self, service):
        self.services.append(service)


    def msg(self, type: str, **msg):
        """
        Send a message upstream.

        Arguments:
            type (str): Message type
            kwargs (dict): Message fields
        """
        msg = {
            'id': self.id,
            'type': type,
            **msg,
        }
        for service in self.services:
            service.msg(**msg)
        self.upstream.send(msg)


    def init(self, taskdef) -> None:
        """
        Send a task initialization message.

        Arguments:
            taskdef (TaskDefinition): New task definition
        """
        self.msg('init', task=taskdef.serialize())


    def run(self) -> None:
        """ Send status update: Running """
        self.msg('status', status=WORK)


    def stop(self, id=None) -> None:
        """ Send status update: Stopped """
        self.msg('status', status=STOP, id=id)
        self.msg('return', result={}, id=id)


    def done(self, result: Any) -> None:
        """ 
        Send status update: Done, and return a result.

        Arguments:
            result (any): Any json-serializable data to return to the upstream task.
        """
        self.msg('status', status=DONE)
        self.msg('return', result=result)


    def fail(self, error: str) -> None:
        """
        Send an error.

        Arguments:
            error (str): Error message
        """
        self.msg('status', status=FAIL)
        self.msg('fail',   error=error)


    def log(self, file: str, data: str) -> None:
        """
        Send captured log output.

        Arguments:
            file (str): Capture source (stdout/stderr)
            data (str): Captured output data
        """
        self.msg('log', file=file, data=data)
