class HotpotQARetriever(BaseRetriever):
    """
    This is a mocked retriever for HotpotQA dataset. It is only meant to be used
    with the hotpotqa dev dataset in the distractor setting. This is the setting that
    does not require retrieval but requires identifying the supporting facts from
    a list of 10 sources.
    """

    def __init__(self, query_objects: Any) -> None:
        assert isinstance(
            query_objects,
            list,
        ), f"query_objects must be a list, got: {type(query_objects)}"
        self._queries = {}
        for object in query_objects:
            self._queries[object["question"]] = object

    def _retrieve(self, query: QueryBundle) -> List[NodeWithScore]:
        if query.custom_embedding_strs:
            query_str = query.custom_embedding_strs[0]
        else:
            query_str = query.query_str
        contexts = self._queries[query_str]["context"]
        node_with_scores = []
        for ctx in contexts:
            text_list = ctx[1]
            text = "\n".join(text_list)
            node = TextNode(text=text, metadata={"title": ctx[0]})
            node_with_scores.append(NodeWithScore(node=node, score=1.0))

        return node_with_scores

    def __str__(self) -> str:
        return "HotpotQARetriever"
