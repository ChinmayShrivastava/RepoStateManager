class KeywordExtractor(BaseExtractor):
    """Keyword extractor. Node-level extractor. Extracts
    `excerpt_keywords` metadata field.

    Args:
        llm (Optional[LLM]): LLM
        keywords (int): number of keywords to extract
    """

    llm: LLMPredictorType = Field(description="The LLM to use for generation.")
    keywords: int = Field(
        default=5, description="The number of keywords to extract.", gt=0
    )

    def __init__(
        self,
        llm: Optional[LLM] = None,
        # TODO: llm_predictor arg is deprecated
        llm_predictor: Optional[LLMPredictorType] = None,
        keywords: int = 5,
        num_workers: int = DEFAULT_NUM_WORKERS,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        if keywords < 1:
            raise ValueError("num_keywords must be >= 1")

        super().__init__(
            llm=llm or llm_predictor or resolve_llm("default"),
            keywords=keywords,
            num_workers=num_workers,
            **kwargs,
        )

    @classmethod
    def class_name(cls) -> str:
        return "KeywordExtractor"

    async def _aextract_keywords_from_node(self, node: BaseNode) -> Dict[str, str]:
        """Extract keywords from a node and return it's metadata dict."""
        if self.is_text_node_only and not isinstance(node, TextNode):
            return {}

        # TODO: figure out a good way to allow users to customize keyword template
        keywords = await self.llm.apredict(
            PromptTemplate(
                template=f"""\
{{context_str}}. Give {self.keywords} unique keywords for this \
document. Format as comma separated. Keywords: """
            ),
            context_str=cast(TextNode, node).text,
        )

        return {"excerpt_keywords": keywords.strip()}

    async def aextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
        keyword_jobs = []
        for node in nodes:
            keyword_jobs.append(self._aextract_keywords_from_node(node))

        metadata_list: List[Dict] = await run_jobs(
            keyword_jobs, show_progress=self.show_progress, workers=self.num_workers
        )

        return metadata_list
