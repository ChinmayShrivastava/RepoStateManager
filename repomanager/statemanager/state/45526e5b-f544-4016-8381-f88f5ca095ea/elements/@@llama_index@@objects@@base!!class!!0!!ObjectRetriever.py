class ObjectRetriever(Generic[OT]):
    """Object retriever."""

    def __init__(
        self, retriever: BaseRetriever, object_node_mapping: BaseObjectNodeMapping[OT]
    ):
        self._retriever = retriever
        self._object_node_mapping = object_node_mapping

    def retrieve(self, str_or_query_bundle: QueryType) -> List[OT]:
        nodes = self._retriever.retrieve(str_or_query_bundle)
        return [self._object_node_mapping.from_node(node.node) for node in nodes]
