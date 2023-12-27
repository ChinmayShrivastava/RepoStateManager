class DecomposeQueryTransform(BaseQueryTransform):
    """Decompose query transform.

    Decomposes query into a subquery given the current index struct.
    Performs a single step transformation.

    Args:
        llm_predictor (Optional[LLM]): LLM for generating
            hypothetical documents

    """

    def __init__(
        self,
        llm: Optional[LLMPredictorType] = None,
        decompose_query_prompt: Optional[DecomposeQueryTransformPrompt] = None,
        verbose: bool = False,
    ) -> None:
        """Init params."""
        super().__init__()
        self._llm = llm or resolve_llm("default")
        self._decompose_query_prompt = (
            decompose_query_prompt or DEFAULT_DECOMPOSE_QUERY_TRANSFORM_PROMPT
        )
        self.verbose = verbose

    def _get_prompts(self) -> PromptDictType:
        """Get prompts."""
        return {"decompose_query_prompt": self._decompose_query_prompt}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""
        if "decompose_query_prompt" in prompts:
            self._decompose_query_prompt = prompts["decompose_query_prompt"]

    def _run(self, query_bundle: QueryBundle, metadata: Dict) -> QueryBundle:
        """Run query transform."""
        # currently, just get text from the index structure
        index_summary = cast(str, metadata.get("index_summary", "None"))

        # given the text from the index, we can use the query bundle to generate
        # a new query bundle
        query_str = query_bundle.query_str
        new_query_str = self._llm.predict(
            self._decompose_query_prompt,
            query_str=query_str,
            context_str=index_summary,
        )

        if self.verbose:
            print_text(f"> Current query: {query_str}\n", color="yellow")
            print_text(f"> New query: {new_query_str}\n", color="pink")

        return QueryBundle(
            query_str=new_query_str,
            custom_embedding_strs=[new_query_str],
        )
