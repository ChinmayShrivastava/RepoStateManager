class SummaryIndexEmbeddingRetriever(BaseRetriever):
    """Embedding based retriever for SummaryIndex.

    Generates embeddings in a lazy fashion for all
    nodes that are traversed.

    Args:
        index (SummaryIndex): The index to retrieve from.
        similarity_top_k (Optional[int]): The number of top nodes to return.

    """

    def __init__(
        self,
        index: SummaryIndex,
        similarity_top_k: Optional[int] = 1,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        self._index = index
        self._similarity_top_k = similarity_top_k
        super().__init__(callback_manager)

    def _retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:
        """Retrieve nodes."""
        node_ids = self._index.index_struct.nodes
        # top k nodes
        nodes = self._index.docstore.get_nodes(node_ids)
        query_embedding, node_embeddings = self._get_embeddings(query_bundle, nodes)

        top_similarities, top_idxs = get_top_k_embeddings(
            query_embedding,
            node_embeddings,
            similarity_top_k=self._similarity_top_k,
            embedding_ids=list(range(len(nodes))),
        )

        top_k_nodes = [nodes[i] for i in top_idxs]

        node_with_scores = []
        for node, similarity in zip(top_k_nodes, top_similarities):
            node_with_scores.append(NodeWithScore(node=node, score=similarity))

        logger.debug(f"> Top {len(top_idxs)} nodes:\n")
        nl = "\n"
        logger.debug(f"{ nl.join([n.get_content() for n in top_k_nodes]) }")
        return node_with_scores

    def _get_embeddings(
        self, query_bundle: QueryBundle, nodes: List[BaseNode]
    ) -> Tuple[List[float], List[List[float]]]:
        """Get top nodes by similarity to the query."""
        if query_bundle.embedding is None:
            query_bundle.embedding = (
                self._index._service_context.embed_model.get_agg_embedding_from_queries(
                    query_bundle.embedding_strs
                )
            )

        node_embeddings: List[List[float]] = []
        nodes_embedded = 0
        for node in nodes:
            if node.embedding is None:
                nodes_embedded += 1
                node.embedding = (
                    self._index.service_context.embed_model.get_text_embedding(
                        node.get_content(metadata_mode=MetadataMode.EMBED)
                    )
                )

            node_embeddings.append(node.embedding)
        return query_bundle.embedding, node_embeddings
