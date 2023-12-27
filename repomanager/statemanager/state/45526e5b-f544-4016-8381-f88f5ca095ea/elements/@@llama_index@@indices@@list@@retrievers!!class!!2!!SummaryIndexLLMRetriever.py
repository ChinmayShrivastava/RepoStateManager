class SummaryIndexLLMRetriever(BaseRetriever):
    """LLM retriever for SummaryIndex.

    Args:
        index (SummaryIndex): The index to retrieve from.
        choice_select_prompt (Optional[PromptTemplate]): A Choice-Select Prompt
           (see :ref:`Prompt-Templates`).)
        choice_batch_size (int): The number of nodes to query at a time.
        format_node_batch_fn (Optional[Callable]): A function that formats a
            batch of nodes.
        parse_choice_select_answer_fn (Optional[Callable]): A function that parses the
            choice select answer.
        service_context (Optional[ServiceContext]): A service context.

    """

    def __init__(
        self,
        index: SummaryIndex,
        choice_select_prompt: Optional[PromptTemplate] = None,
        choice_batch_size: int = 10,
        format_node_batch_fn: Optional[Callable] = None,
        parse_choice_select_answer_fn: Optional[Callable] = None,
        service_context: Optional[ServiceContext] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        self._index = index
        self._choice_select_prompt = (
            choice_select_prompt or DEFAULT_CHOICE_SELECT_PROMPT
        )
        self._choice_batch_size = choice_batch_size
        self._format_node_batch_fn = (
            format_node_batch_fn or default_format_node_batch_fn
        )
        self._parse_choice_select_answer_fn = (
            parse_choice_select_answer_fn or default_parse_choice_select_answer_fn
        )
        self._service_context = service_context or index.service_context
        super().__init__(callback_manager)

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve nodes."""
        node_ids = self._index.index_struct.nodes
        results = []
        for idx in range(0, len(node_ids), self._choice_batch_size):
            node_ids_batch = node_ids[idx : idx + self._choice_batch_size]
            nodes_batch = self._index.docstore.get_nodes(node_ids_batch)

            query_str = query_bundle.query_str
            fmt_batch_str = self._format_node_batch_fn(nodes_batch)
            # call each batch independently
            raw_response = self._service_context.llm.predict(
                self._choice_select_prompt,
                context_str=fmt_batch_str,
                query_str=query_str,
            )

            raw_choices, relevances = self._parse_choice_select_answer_fn(
                raw_response, len(nodes_batch)
            )
            choice_idxs = [int(choice) - 1 for choice in raw_choices]
            choice_node_ids = [node_ids_batch[idx] for idx in choice_idxs]

            choice_nodes = self._index.docstore.get_nodes(choice_node_ids)
            relevances = relevances or [1.0 for _ in choice_nodes]
            results.extend(
                [
                    NodeWithScore(node=node, score=relevance)
                    for node, relevance in zip(choice_nodes, relevances)
                ]
            )
        return results
