class KG(IndexStruct):
    """A table of keywords mapping keywords to text chunks."""

    # Unidirectional

    # table of keywords to node ids
    table: Dict[str, Set[str]] = field(default_factory=dict)

    # TODO: legacy attribute, remove in future releases
    rel_map: Dict[str, List[List[str]]] = field(default_factory=dict)

    # TBD, should support vector store, now we just persist the embedding memory
    # maybe chainable abstractions for *_stores could be designed
    embedding_dict: Dict[str, List[float]] = field(default_factory=dict)

    @property
    def node_ids(self) -> Set[str]:
        """Get all node ids."""
        return set.union(*self.table.values())

    def add_to_embedding_dict(self, triplet_str: str, embedding: List[float]) -> None:
        """Add embedding to dict."""
        self.embedding_dict[triplet_str] = embedding

    def add_node(self, keywords: List[str], node: BaseNode) -> None:
        """Add text to table."""
        node_id = node.node_id
        for keyword in keywords:
            if keyword not in self.table:
                self.table[keyword] = set()
            self.table[keyword].add(node_id)

    def search_node_by_keyword(self, keyword: str) -> List[str]:
        """Search for nodes by keyword."""
        if keyword not in self.table:
            return []
        return list(self.table[keyword])

    @classmethod
    def get_type(cls) -> IndexStructType:
        """Get type."""
        return IndexStructType.KG
