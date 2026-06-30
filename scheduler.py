class Scheduler:
    """
    GCON Job Scheduler.

    Selects an available node from the NodeRegistry.
    """

    def __init__(self, registry):
        """
        Initialize the scheduler.

        Args:
            registry (NodeRegistry): The node registry.
        """
        self.registry = registry

    def select_node(self):
        """
        Select the next available node.

        Returns:
            GCONAgent: An idle node, or None if no nodes are available.
        """

        available = self.registry.available_nodes()

        if not available:
            return None

        return available[0]

    def has_available_node(self):
        """
        Check whether an idle node exists.

        Returns:
            bool
        """

        return len(self.registry.available_nodes()) > 0

    def node_count(self):
        """
        Return the number of registered nodes.
        """

        return len(self.registry.list_nodes())