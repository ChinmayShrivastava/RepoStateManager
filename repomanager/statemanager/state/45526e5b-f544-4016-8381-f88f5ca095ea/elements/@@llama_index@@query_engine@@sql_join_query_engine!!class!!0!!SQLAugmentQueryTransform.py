class SQLAugmentQueryTransform(BaseQueryTransform):
    """SQL Augment Query Transform.

    This query transform will transform the query into a more specific query
    after augmenting with SQL results.

    Args:
        llm (LLM): LLM to use for query transformation.
        sql_augment_transform_prompt (BasePromptTemplate): PromptTemplate to use
            for query transformation.
        check_stop_parser (Optional[Callable[[str], bool]]): Check stop function.

    """

    def __init__(
        self,
        llm: Optional[LLMPredictorType] = None,
        sql_augment_transform_prompt: Optional[BasePromptTemplate] = None,
        check_stop_parser: Optional[Callable[[QueryBundle], bool]] = None,
    ) -> None:
        """Initialize params."""
        self._llm = llm or resolve_llm("default")

        self._sql_augment_transform_prompt = (
            sql_augment_transform_prompt or DEFAULT_SQL_AUGMENT_TRANSFORM_PROMPT
        )
        self._check_stop_parser = check_stop_parser or _default_check_stop

    def _get_prompts(self) -> PromptDictType:
        """Get prompts."""
        return {"sql_augment_transform_prompt": self._sql_augment_transform_prompt}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""
        if "sql_augment_transform_prompt" in prompts:
            self._sql_augment_transform_prompt = prompts["sql_augment_transform_prompt"]

    def _run(self, query_bundle: QueryBundle, metadata: Dict) -> QueryBundle:
        """Run query transform."""
        query_str = query_bundle.query_str
        sql_query = metadata["sql_query"]
        sql_query_response = metadata["sql_query_response"]
        new_query_str = self._llm.predict(
            self._sql_augment_transform_prompt,
            query_str=query_str,
            sql_query_str=sql_query,
            sql_response_str=sql_query_response,
        )
        return QueryBundle(
            new_query_str, custom_embedding_strs=query_bundle.custom_embedding_strs
        )

    def check_stop(self, query_bundle: QueryBundle) -> bool:
        """Check if query indicates stop."""
        return self._check_stop_parser(query_bundle)
