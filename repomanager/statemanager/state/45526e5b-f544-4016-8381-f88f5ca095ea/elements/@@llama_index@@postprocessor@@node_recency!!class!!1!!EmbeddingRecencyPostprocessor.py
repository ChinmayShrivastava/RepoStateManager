class EmbeddingRecencyPostprocessor(BaseNodePostprocessor):
    """Recency post-processor.

    This post-processor does the following steps:

    - Decides if we need to use the post-processor given the query
      (is it temporal-related?)
    - If yes, sorts nodes by date.
    - For each node, look at subsequent nodes and filter out nodes
      that have high embedding similarity with the current node.
      Because this means the subsequent node may have overlapping content
      with the current node but is also out of date
    """

    service_context: ServiceContext
    # infer_recency_tmpl: str = Field(default=DEFAULT_INFER_RECENCY_TMPL)
    date_key: str = "date"
    similarity_cutoff: float = Field(default=0.7)
    query_embedding_tmpl: str = Field(default=DEFAULT_QUERY_EMBEDDING_TMPL)

    @classmethod
    def class_name(cls) -> str:
        return "EmbeddingRecencyPostprocessor"

    def _postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        """Postprocess nodes."""
        if query_bundle is None:
            raise ValueError("Missing query bundle in extra info.")

        # sort nodes by date
        node_dates = pd.to_datetime(
            [node.node.metadata[self.date_key] for node in nodes]
        )
        sorted_node_idxs = np.flip(node_dates.argsort())
        sorted_nodes: List[NodeWithScore] = [nodes[idx] for idx in sorted_node_idxs]

        # get embeddings for each node
        embed_model = self.service_context.embed_model
        texts = [node.get_content(metadata_mode=MetadataMode.EMBED) for node in nodes]
        text_embeddings = embed_model.get_text_embedding_batch(texts=texts)

        node_ids_to_skip: Set[str] = set()
        for idx, node in enumerate(sorted_nodes):
            if node.node.node_id in node_ids_to_skip:
                continue
            # get query embedding for the "query" node
            # NOTE: not the same as the text embedding because
            # we want to optimize for retrieval results

            query_text = self.query_embedding_tmpl.format(
                context_str=node.node.get_content(metadata_mode=MetadataMode.EMBED),
            )
            query_embedding = embed_model.get_query_embedding(query_text)

            for idx2 in range(idx + 1, len(sorted_nodes)):
                if sorted_nodes[idx2].node.node_id in node_ids_to_skip:
                    continue
                node2 = sorted_nodes[idx2]
                if (
                    np.dot(query_embedding, text_embeddings[idx2])
                    > self.similarity_cutoff
                ):
                    node_ids_to_skip.add(node2.node.node_id)

        return [
            node for node in sorted_nodes if node.node.node_id not in node_ids_to_skip
        ]
