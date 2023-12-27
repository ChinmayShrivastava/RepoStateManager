class IndexDict(IndexStruct):
    """A simple dictionary of documents."""

    # TODO: slightly deprecated, should likely be a list or set now
    # mapping from vector store id to node doc_id
    nodes_dict: Dict[str, str] = field(default_factory=dict)

    # TODO: deprecated, not used
    # mapping from node doc_id to vector store id
    doc_id_dict: Dict[str, List[str]] = field(default_factory=dict)

    # TODO: deprecated, not used
    # this should be empty for all other indices
    embeddings_dict: Dict[str, List[float]] = field(default_factory=dict)

    def add_node(
        self,
        node: BaseNode,
        text_id: Optional[str] = None,
    ) -> str:
        """Add text to table, return current position in list."""
        # # don't worry about child indices for now, nodes are all in order
        # self.nodes_dict[int_id] = node
        vector_id = text_id if text_id is not None else node.node_id
        self.nodes_dict[vector_id] = node.node_id

        return vector_id

    def delete(self, doc_id: str) -> None:
        """Delete a Node."""
        del self.nodes_dict[doc_id]

    @classmethod
    def get_type(cls) -> IndexStructType:
        """Get type."""
        return IndexStructType.VECTOR_STORE
