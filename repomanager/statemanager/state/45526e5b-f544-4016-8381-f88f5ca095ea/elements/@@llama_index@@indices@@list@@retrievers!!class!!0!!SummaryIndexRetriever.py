class SummaryIndexRetriever(BaseRetriever):
    """Simple retriever for SummaryIndex that returns all nodes.

    Args:
        index (SummaryIndex): The index to retrieve from.

    """

    def __init__(
        self,
        index: SummaryIndex,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        self._index = index
        super().__init__(callback_manager)

    def _retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
        """Retrieve nodes."""
        del query_bundle

        node_ids = self._index.index_struct.nodes
        nodes = self._index.docstore.get_nodes(node_ids)
        return [NodeWithScore(node=node) for node in nodes]
