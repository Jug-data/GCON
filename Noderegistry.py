class NodeRegistry:
    """
    Stores and manages GCON nodes.
    """

    def __init__(self):
        self.nodes = {}
        
    def register(self, node):
        """
        Register a new node.
        """

        if node.node_id in self.nodes:
            raise ValueError(f"Node '{node.node_id}' already exists.")

        self.nodes[node.node_id] = node
        
    def remove(self, node_id):
        """
        Remove a node from the registry.
        """

        if node_id not in self.nodes:
            raise ValueError(f"Node '{node_id}' does not exist.")

        del self.nodes[node_id] 
        
    def get_node(self, node_id):
        """
        Return a node by ID.
        """

        if node_id not in self.nodes:
             raise ValueError(f"Node '{node_id}' does not exist.")

        return self.nodes[node_id]
    
    def list_nodes(self):
        """
        Return all registered node IDs.
        """

        return list(self.nodes.keys())
    
    def available_nodes(self):
        """
        Return all idle nodes.
        """

        return [     
            
        node
        for node in self.nodes.values()
        if node.status == "idle"
    ]