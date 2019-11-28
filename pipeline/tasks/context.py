from .definition import TaskDefinition


class TaskContext(TaskDefinition):
    """
    Task Execution Context

    Attributes:
        cluster (ClusterProvider): Cluster provider
        node (WorkerNode): Network node
        id (str): Task id
        name (str): Task name
        image (str): Task image
        parent (str): Parent task id
        inputs (dict): Input arguments
        config (dict): Configuration variables
        upstream (str): Upstream connection string
    """

    def __init__(
        self,
        taskdef: TaskDefinition,
        cluster,
        node,
    ):
        """
        Arguments:
            taskdef (TaskDefinition): Task definition
            cluster (ClusterProvider): Cluster connection
            node (WorkerNode): Upstream connection
        """
        kwargs = taskdef.serialize()
        TaskDefinition.__init__(self, **kwargs)
        self.cluster = cluster
        self.node = node
