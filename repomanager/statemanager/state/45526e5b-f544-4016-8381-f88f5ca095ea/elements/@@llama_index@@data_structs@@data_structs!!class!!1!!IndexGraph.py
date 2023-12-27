class IndexGraph(IndexStruct):
    """A graph representing the tree-structured index."""

    # mapping from index in tree to Node doc id.
    all_nodes: Dict[int, str] = field(default_factory=dict)
    root_nodes: Dict[int, str] = field(default_factory=dict)
    node_id_to_children_ids: Dict[str, List[str]] = field(default_factory=dict)

    @property
    def node_id_to_index(self) -> Dict[str, int]:
        """Map from node id to index."""
        return {node_id: index for index, node_id in self.all_nodes.items()}

    @property
    def size(self) -> int:
        """Get the size of the graph."""
        return len(self.all_nodes)

    def get_index(self, node: BaseNode) -> int:
        """Get index of node."""
        return self.node_id_to_index[node.node_id]

    def insert(
        self,
        node: BaseNode,
        index: Optional[int] = None,
        children_nodes: Optional[Sequence[BaseNode]] = None,
    ) -> None:
        """Insert node."""
        index = index or self.size
        node_id = node.node_id

        self.all_nodes[index] = node_id

        if children_nodes is None:
            children_nodes = []
        children_ids = [n.node_id for n in children_nodes]
        self.node_id_to_children_ids[node_id] = children_ids

    def get_children(self, parent_node: Optional[BaseNode]) -> Dict[int, str]:
        """Get children nodes."""
        if parent_node is None:
            return self.root_nodes
        else:
            parent_id = parent_node.node_id
            children_ids = self.node_id_to_children_ids[parent_id]
            return {
                self.node_id_to_index[child_id]: child_id for child_id in children_ids
            }

    def insert_under_parent(
        self,
        node: BaseNode,
        parent_node: Optional[BaseNode],
        new_index: Optional[int] = None,
    ) -> None:
        """Insert under parent node."""
        new_index = new_index or self.size
        if parent_node is None:
            self.root_nodes[new_index] = node.node_id
            self.node_id_to_children_ids[node.node_id] = []
        else:
            if parent_node.node_id not in self.node_id_to_children_ids:
                self.node_id_to_children_ids[parent_node.node_id] = []
            self.node_id_to_children_ids[parent_node.node_id].append(node.node_id)

        self.all_nodes[new_index] = node.node_id

    @classmethod
    def get_type(cls) -> IndexStructType:
        """Get type."""
        return IndexStructType.TREE
