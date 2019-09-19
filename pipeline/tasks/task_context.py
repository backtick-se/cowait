

class TaskContext(object):
    """
    Task Execution Context

    Attributes:
        cluster (ClusterProvider): Cluster provider
        upstream (UpstreamConnector): Upstream connector
        id (str): Task id
        name (str): Task name
        image (str): Task image
        inputs (dict): Input arguments
        config (dict): Configuration variables
        parent (str): Parent connection string
    """

    def __init__(self, 
        cluster,
        upstream,
        taskdef,
    ):
        """
        Arguments:
            cluster (ClusterProvider): Cluster connection
            upstream (UpstreamConnector): Upstream connection
            taskdef (TaskDefinition): Task definition
        """
        self.cluster  = cluster
        self.upstream = upstream

        for key, value in taskdef.serialize().items():
            setattr(self, key, value)