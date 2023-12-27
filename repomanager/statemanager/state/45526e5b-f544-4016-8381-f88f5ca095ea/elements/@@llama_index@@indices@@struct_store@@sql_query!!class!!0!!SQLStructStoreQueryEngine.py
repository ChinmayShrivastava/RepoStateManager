class SQLStructStoreQueryEngine(BaseQueryEngine):
    """GPT SQL query engine over a structured database.

    NOTE: deprecated in favor of SQLTableRetriever, kept for backward compatibility.

    Runs raw SQL over a SQLStructStoreIndex. No LLM calls are made here.
    NOTE: this query cannot work with composed indices - if the index
    contains subindices, those subindices will not be queried.
    """

    def __init__(
        self,
        index: SQLStructStoreIndex,
        sql_context_container: Optional[SQLContextContainerBuilder] = None,
        sql_only: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        self._sql_database = index.sql_database
        self._sql_context_container = (
            sql_context_container or index.sql_context_container
        )
        self._sql_only = sql_only
        super().__init__(index.service_context.callback_manager)

    def _get_prompt_modules(self) -> PromptMixinType:
        """Get prompt modules."""
        return {}

    def _run_with_sql_only_check(
        self, sql_query_str: str
    ) -> Tuple[str, Dict[str, Any]]:
        """Don't run sql if sql_only is true, else continue with normal path."""
        if self._sql_only:
            metadata: Dict[str, Any] = {}
            raw_response_str = sql_query_str
        else:
            raw_response_str, metadata = self._sql_database.run_sql(sql_query_str)

        return raw_response_str, metadata

    def _query(self, query_bundle: QueryBundle) -> Response:
        """Answer a query."""
        # NOTE: override query method in order to fetch the right results.
        # NOTE: since the query_str is a SQL query, it doesn't make sense
        # to use ResponseBuilder anywhere.
        response_str, metadata = self._run_with_sql_only_check(query_bundle.query_str)
        return Response(response=response_str, metadata=metadata)

    async def _aquery(self, query_bundle: QueryBundle) -> Response:
        return self._query(query_bundle)
