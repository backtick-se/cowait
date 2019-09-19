from abc import ABC, abstractmethod
from typing import Any


class UpstreamConnector(ABC):
    def __init__(self, id):
        super().__init__()
        self.id = id


    @abstractmethod
    def msg(self, type: str, **msg):
        """
        Send a message upstream.

        Arguments:
            type (str): Message type
            kwargs (dict): Message fields
        """
        pass


    def init(self, taskdef) -> None:
        """
        Send a task initialization message.

        Arguments:
            taskdef (TaskDefinition): New task definition
        """
        self.msg('init', task=taskdef.serialize())


    def run(self) -> None:
        """ Send status update: Running """
        self.msg('status', status='run')


    def stop(self) -> None:
        """ Send status update: Stopped """
        self.msg('status', status='stop')
        self.msg('return', result={})


    def done(self, result: Any) -> None:
        """ 
        Send status update: Done, and return a result.

        Arguments:
            result (any): Any json-serializable data to return to the parent task.
        """
        self.msg('status', status='done')
        self.msg('return', result=result)


    def fail(self, error: str) -> None:
        """
        Send an error.

        Arguments:
            error (str): Error message
        """
        self.msg('status', status='error')
        self.msg('fail',   error=error)


    def log(self, file: str, data: str) -> None:
        """
        Send captured log output.

        Arguments:
            file (str): Capture source (stdout/stderr)
            data (str): Captured output data
        """
        self.msg('log', file=file, data=data)
