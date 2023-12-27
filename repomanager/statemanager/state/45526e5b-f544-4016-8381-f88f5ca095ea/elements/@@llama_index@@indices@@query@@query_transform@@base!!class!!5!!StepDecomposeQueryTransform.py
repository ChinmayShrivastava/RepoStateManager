class StepDecomposeQueryTransform(BaseQueryTransform):
    """Step decompose query transform.

    Decomposes query into a subquery given the current index struct
    and previous reasoning.

    NOTE: doesn't work yet.

    Args:
        llm_predictor (Optional[LLM]): LLM for generating
            hypothetical documents

    """

    def __init__(
        self,
        llm: Optional[LLMPredictorType] = None,
        step_decompose_query_prompt: Optional[StepDecomposeQueryTransformPrompt] = None,
        verbose: bool = False,
    ) -> None:
        """Init params."""
        super().__init__()
        self._llm = llm or resolve_llm("default")
        self._step_decompose_query_prompt = (
            step_decompose_query_prompt or DEFAULT_STEP_DECOMPOSE_QUERY_TRANSFORM_PROMPT
        )
        self.verbose = verbose

    def _get_prompts(self) -> PromptDictType:
        """Get prompts."""
        return {"step_decompose_query_prompt": self._step_decompose_query_prompt}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""
        if "step_decompose_query_prompt" in prompts:
            self._step_decompose_query_prompt = prompts["step_decompose_query_prompt"]

    def _run(self, query_bundle: QueryBundle, metadata: Dict) -> QueryBundle:
        """Run query transform."""
        index_summary = cast(
            str,
            metadata.get("index_summary", "None"),
        )
        prev_reasoning = cast(Response, metadata.get("prev_reasoning"))
        fmt_prev_reasoning = f"\n{prev_reasoning}" if prev_reasoning else "None"

        # given the text from the index, we can use the query bundle to generate
        # a new query bundle
        query_str = query_bundle.query_str
        new_query_str = self._llm.predict(
            self._step_decompose_query_prompt,
            prev_reasoning=fmt_prev_reasoning,
            query_str=query_str,
            context_str=index_summary,
        )
        if self.verbose:
            print_text(f"> Current query: {query_str}\n", color="yellow")
            print_text(f"> New query: {new_query_str}\n", color="pink")
        return QueryBundle(
            query_str=new_query_str,
            custom_embedding_strs=query_bundle.custom_embedding_strs,
        )
