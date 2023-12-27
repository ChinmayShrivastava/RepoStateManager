class FixedRecencyPostprocessor(BaseNodePostprocessor):
    """Recency post-processor.

    This post-processor does the following steps:

    - Decides if we need to use the post-processor given the query
      (is it temporal-related?)
    - If yes, sorts nodes by date.
    - Take the first k nodes (by default 1), and use that to synthesize an answer.

    """

    service_context: ServiceContext
    top_k: int = 1
    # infer_recency_tmpl: str = Field(default=DEFAULT_INFER_RECENCY_TMPL)
    date_key: str = "date"

    @classmethod
    def class_name(cls) -> str:
        return "FixedRecencyPostprocessor"

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
        sorted_nodes = [nodes[idx] for idx in sorted_node_idxs]

        return sorted_nodes[: self.top_k]
