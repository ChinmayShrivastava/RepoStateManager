class DocumentSummaryIndexEmbeddingRetriever(BaseRetriever):
    """Document Summary Index Embedding Retriever.

    Args:
        index (DocumentSummaryIndex): The index to retrieve from.
        similarity_top_k (int): The number of summary nodes to retrieve.

    """

    def __init__(
        self,
        index: DocumentSummaryIndex,
        similarity_top_k: int = 1,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        self._index = index
        self._vector_store = self._index.vector_store
        self._service_context = self._index.service_context
        self._docstore = self._index.docstore
        self._index_struct = self._index.index_struct
        self._similarity_top_k = similarity_top_k
        super().__init__(callback_manager)

    def _retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
        """Retrieve nodes."""
        if self._vector_store.is_embedding_query:
            if query_bundle.embedding is None:
                query_bundle.embedding = (
                    self._service_context.embed_model.get_agg_embedding_from_queries(
                        query_bundle.embedding_strs
                    )
                )

        query = VectorStoreQuery(
            query_embedding=query_bundle.embedding,
            similarity_top_k=self._similarity_top_k,
        )
        query_result = self._vector_store.query(query)

        top_k_summary_ids: List[str]
        if query_result.ids is not None:
            top_k_summary_ids = query_result.ids
        elif query_result.nodes is not None:
            top_k_summary_ids = [n.node_id for n in query_result.nodes]
        else:
            raise ValueError(
                "Vector store query result should return "
                "at least one of nodes or ids."
            )

        results = []
        for summary_id in top_k_summary_ids:
            node_ids = self._index_struct.summary_id_to_node_ids[summary_id]
            nodes = self._docstore.get_nodes(node_ids)
            results.extend([NodeWithScore(node=n) for n in nodes])
        return results
