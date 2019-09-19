

class TaskContext(object):
    def __init__(self, 
        cluster, 
        upstream, 
        taskdef,
    ):
        """
        Arguments:
            id (str): Task id
            parent (str): Parent task id (or None if root)
            cluster (ClusterProvider): Cluster connection
            upstream: Upstream connection
        """
        self.cluster  = cluster
        self.upstream = upstream
        self.id       = taskdef.id
        self.name     = taskdef.name
        self.inputs   = taskdef.inputs
        self.config   = taskdef.config
        self.parent   = taskdef.parent