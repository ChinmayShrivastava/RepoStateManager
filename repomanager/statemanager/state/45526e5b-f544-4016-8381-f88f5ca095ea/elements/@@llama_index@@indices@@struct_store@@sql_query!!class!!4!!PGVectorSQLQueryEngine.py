class PGVectorSQLQueryEngine(BaseSQLTableQueryEngine):
    """PGvector SQL query engine.

    A modified version of the normal text-to-SQL query engine because
    we can infer embedding vectors in the sql query.

    NOTE: this is a beta feature

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
        text_to_sql_prompt = text_to_sql_prompt or DEFAULT_TEXT_TO_SQL_PGVECTOR_PROMPT
        self._sql_retriever = NLSQLRetriever(
            sql_database,
            text_to_sql_prompt=text_to_sql_prompt,
            context_query_kwargs=context_query_kwargs,
            tables=tables,
            sql_parser_mode=SQLParserMode.PGVECTOR,
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
