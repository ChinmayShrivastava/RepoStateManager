class SQLDocumentContextBuilder:
    """Builder that builds context for a given set of SQL tables.

    Args:
        sql_database (Optional[SQLDatabase]): SQL database to use,
        llm_predictor (Optional[BaseLLMPredictor]): LLM Predictor to use.
        prompt_helper (Optional[PromptHelper]): Prompt Helper to use.
        text_splitter (Optional[TextSplitter]): Text Splitter to use.
        table_context_prompt (Optional[BasePromptTemplate]): A
            Table Context Prompt (see :ref:`Prompt-Templates`).
        refine_table_context_prompt (Optional[BasePromptTemplate]):
            A Refine Table Context Prompt (see :ref:`Prompt-Templates`).
        table_context_task (Optional[str]): The query to perform
            on the table context. A default query string is used
            if none is provided by the user.
    """

    def __init__(
        self,
        sql_database: SQLDatabase,
        service_context: Optional[ServiceContext] = None,
        text_splitter: Optional[TextSplitter] = None,
        table_context_prompt: Optional[BasePromptTemplate] = None,
        refine_table_context_prompt: Optional[BasePromptTemplate] = None,
        table_context_task: Optional[str] = None,
    ) -> None:
        """Initialize params."""
        # TODO: take in an entire index instead of forming a response builder
        if sql_database is None:
            raise ValueError("sql_database must be provided.")
        self._sql_database = sql_database
        self._text_splitter = text_splitter
        self._service_context = service_context or ServiceContext.from_defaults()
        self._table_context_prompt = (
            table_context_prompt or DEFAULT_TABLE_CONTEXT_PROMPT
        )
        self._refine_table_context_prompt = (
            refine_table_context_prompt or DEFAULT_REFINE_TABLE_CONTEXT_PROMPT_SEL
        )
        self._table_context_task = table_context_task or DEFAULT_TABLE_CONTEXT_QUERY

    def build_all_context_from_documents(
        self,
        documents_dict: Dict[str, List[BaseNode]],
    ) -> Dict[str, str]:
        """Build context for all tables in the database."""
        context_dict = {}
        for table_name in self._sql_database.get_usable_table_names():
            context_dict[table_name] = self.build_table_context_from_documents(
                documents_dict[table_name], table_name
            )
        return context_dict

    def build_table_context_from_documents(
        self,
        documents: Sequence[BaseNode],
        table_name: str,
    ) -> str:
        """Build context from documents for a single table."""
        schema = self._sql_database.get_single_table_info(table_name)
        prompt_with_schema = self._table_context_prompt.partial_format(schema=schema)
        prompt_with_schema.metadata["prompt_type"] = PromptType.QUESTION_ANSWER
        refine_prompt_with_schema = self._refine_table_context_prompt.partial_format(
            schema=schema
        )
        refine_prompt_with_schema.metadata["prompt_type"] = PromptType.REFINE

        text_splitter = (
            self._text_splitter
            or self._service_context.prompt_helper.get_text_splitter_given_prompt(
                prompt_with_schema
            )
        )
        # we use the ResponseBuilder to iteratively go through all texts
        response_builder = get_response_synthesizer(
            service_context=self._service_context,
            text_qa_template=prompt_with_schema,
            refine_template=refine_prompt_with_schema,
        )
        with self._service_context.callback_manager.event(
            CBEventType.CHUNKING,
            payload={EventPayload.DOCUMENTS: documents},
        ) as event:
            text_chunks = []
            for doc in documents:
                chunks = text_splitter.split_text(
                    doc.get_content(metadata_mode=MetadataMode.LLM)
                )
                text_chunks.extend(chunks)

            event.on_end(
                payload={EventPayload.CHUNKS: text_chunks},
            )

        # feed in the "query_str" or the task
        table_context = response_builder.get_response(
            text_chunks=text_chunks, query_str=self._table_context_task
        )
        return cast(str, table_context)
