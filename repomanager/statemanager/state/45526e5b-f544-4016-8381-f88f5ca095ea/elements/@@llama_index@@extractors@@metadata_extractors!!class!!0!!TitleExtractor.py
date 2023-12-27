class TitleExtractor(BaseExtractor):
    """Title extractor. Useful for long documents. Extracts `document_title`
    metadata field.

    Args:
        llm (Optional[LLM]): LLM
        nodes (int): number of nodes from front to use for title extraction
        node_template (str): template for node-level title clues extraction
        combine_template (str): template for combining node-level clues into
            a document-level title
    """

    is_text_node_only: bool = False  # can work for mixture of text and non-text nodes
    llm: LLMPredictorType = Field(description="The LLM to use for generation.")
    nodes: int = Field(
        default=5,
        description="The number of nodes to extract titles from.",
        gt=0,
    )
    node_template: str = Field(
        default=DEFAULT_TITLE_NODE_TEMPLATE,
        description="The prompt template to extract titles with.",
    )
    combine_template: str = Field(
        default=DEFAULT_TITLE_COMBINE_TEMPLATE,
        description="The prompt template to merge titles with.",
    )

    def __init__(
        self,
        llm: Optional[LLM] = None,
        # TODO: llm_predictor arg is deprecated
        llm_predictor: Optional[LLMPredictorType] = None,
        nodes: int = 5,
        node_template: str = DEFAULT_TITLE_NODE_TEMPLATE,
        combine_template: str = DEFAULT_TITLE_COMBINE_TEMPLATE,
        num_workers: int = DEFAULT_NUM_WORKERS,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        if nodes < 1:
            raise ValueError("num_nodes must be >= 1")

        super().__init__(
            llm=llm or llm_predictor or resolve_llm("default"),
            nodes=nodes,
            node_template=node_template,
            combine_template=combine_template,
            num_workers=num_workers,
            **kwargs,
        )

    @classmethod
    def class_name(cls) -> str:
        return "TitleExtractor"

    async def aextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
        nodes_to_extract_title: List[BaseNode] = []

        for node in nodes:
            if len(nodes_to_extract_title) >= self.nodes:
                break
            if self.is_text_node_only and not isinstance(node, TextNode):
                continue
            nodes_to_extract_title.append(node)

        if len(nodes_to_extract_title) == 0:
            # Could not extract title
            return []

        title_jobs = [
            self.llm.apredict(
                PromptTemplate(template=self.node_template),
                context_str=cast(TextNode, node).text,
            )
            for node in nodes_to_extract_title
        ]
        title_candidates = await run_jobs(
            title_jobs, show_progress=self.show_progress, workers=self.num_workers
        )

        if len(nodes_to_extract_title) > 1:
            titles = reduce(
                lambda x, y: x + "," + y, title_candidates[1:], title_candidates[0]
            )

            title = await self.llm.apredict(
                PromptTemplate(template=self.combine_template),
                context_str=titles,
            )
        else:
            title = title_candidates[
                0
            ]  # if single node, just use the title from that node

        return [{"document_title": title.strip(' \t\n\r"')} for _ in nodes]
