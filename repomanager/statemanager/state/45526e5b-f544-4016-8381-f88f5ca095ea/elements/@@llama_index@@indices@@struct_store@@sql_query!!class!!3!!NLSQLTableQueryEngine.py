class NLSQLTableQueryEngine(BaseSQLTableQueryEngine):
    """
    Natural language SQL Table query engine.

    Read NLStructStoreQueryEngine's docstring for more info on NL SQL.
    """

    def __init__(
        self,
        sql_database: SQLDatabase,
        text_to_sql_prompt: Optional[BasePromptTemplate] = None,
        context_query_kwargs: Optional[dict] = None,
        synthesize_response: bool = True,
        response_synthesis_prompt: Optional[BasePromptTemplate] = None,
        tables: Optional[Union[List[str], List[Table]]] = None,
        service_context: Optional[ServiceContext] = None,
        context_str_prefix: Optional[str] = None,
        sql_only: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        # self._tables = tables
        self._sql_retriever = NLSQLRetriever(
            sql_database,
            text_to_sql_prompt=text_to_sql_prompt,
            context_query_kwargs=context_query_kwargs,
            tables=tables,
            context_str_prefix=context_str_prefix,
            service_context=service_context,
            sql_only=sql_only,
        )
        super().__init__(
            synthesize_response=synthesize_response,
            response_synthesis_prompt=response_synthesis_prompt,
            service_context=service_context,
            **kwargs,
        )

    @property
    def sql_retriever(self) -> NLSQLRetriever:
        """Get SQL retriever."""
        return self._sql_retriever
