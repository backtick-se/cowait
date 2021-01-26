Module cowait.worker.worker_node
================================

Classes
-------

`WorkerNode(id: str, upstream: str, port: int = 80, logger: cowait.worker.logger.logger.Logger = None)`
:   

    ### Methods

    `capture_logs(self) ‑> cowait.utils.stream_capture.StreamCapturing`
    :   Sets up a stream capturing context, forwarding logs to the node

    `close(self) ‑> NoneType`
    :

    `connect(self) ‑> NoneType`
    :

    `get_url(self)`
    :

    `monitor_system(self, interval: float = 1.0)`
    :

    `serve(self)`
    :