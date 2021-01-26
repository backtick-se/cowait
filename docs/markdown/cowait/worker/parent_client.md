Module cowait.worker.parent_client
==================================

Classes
-------

`ParentClient(id, io_loop, logger: cowait.worker.logger.logger.Logger = None)`
:   Upstream API client.

    ### Ancestors (in MRO)

    * cowait.network.client.Client
    * cowait.utils.emitter.EventEmitter

    ### Methods

    `connect(self, url: str, token: str = None) ‑> NoneType`
    :

    `msg(self, type: str, **msg) ‑> NoneType`
    :   Send a message upstream.
        
        Arguments:
            type (str): Message type
            kwargs (dict): Message fields

    `send(self, msg: dict)`
    :

    `send_done(self, result: Any, result_type: str = 'any') ‑> NoneType`
    :   Send status update: Done, and return a result.
        
        Arguments:
            result (any): Any serializable data to return to the upstream task.
            result_type (str): Result type description

    `send_fail(self, error: str) ‑> NoneType`
    :   Send an error.
        
        Arguments:
            error (str): Error message

    `send_init(self, taskdef: cowait.tasks.definition.TaskDefinition) ‑> NoneType`
    :   Send a task initialization message.
        
        Arguments:
            taskdef (TaskDefinition): New task definition

    `send_log(self, file: str, data: str) ‑> NoneType`
    :   Send captured log output.
        
        Arguments:
            file (str): Capture source (stdout/stderr)
            data (str): Captured output data

    `send_run(self) ‑> NoneType`
    :   Send status update: Running

    `send_stats(self, stats: dict) ‑> NoneType`
    :

    `send_stop(self, id: str = None) ‑> NoneType`
    :   Send status update: Stopped