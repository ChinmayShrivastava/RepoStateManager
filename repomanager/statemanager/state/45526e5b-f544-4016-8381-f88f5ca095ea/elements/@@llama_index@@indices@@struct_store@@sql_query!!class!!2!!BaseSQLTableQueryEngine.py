class BaseSQLTableQueryEngine(BaseQueryEngine):
    def __init__(
        self,
        synthesize_response: bool = True,
        response_synthesis_prompt: Optional[BasePromptTemplate] = None,
        service_context: Optional[ServiceContext] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        self._service_context = service_context or ServiceContext.from_defaults()
        self._response_synthesis_prompt = (
            response_synthesis_prompt or DEFAULT_RESPONSE_SYNTHESIS_PROMPT_V2
        )
        # do some basic prompt validation
        _validate_prompt(self._response_synthesis_prompt)
        self._synthesize_response = synthesize_response
        super().__init__(self._service_context.callback_manager, **kwargs)

    def _get_prompts(self) -> Dict[str, Any]:
        """Get prompts."""
        return {"response_synthesis_prompt": self._response_synthesis_prompt}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""
        if "response_synthesis_prompt" in prompts:
            self._response_synthesis_prompt = prompts["response_synthesis_prompt"]

    def _get_prompt_modules(self) -> PromptMixinType:
        """Get prompt modules."""
        return {"sql_retriever": self.sql_retriever}

    @property
    @abstractmethod
    def sql_retriever(self) -> NLSQLRetriever:
        """Get SQL retriever."""

    @property
    def service_context(self) -> ServiceContext:
        """Get service context."""
        return self._service_context

    def _query(self, query_bundle: QueryBundle) -> Response:
        """Answer a query."""
        retrieved_nodes, metadata = self.sql_retriever.retrieve_with_metadata(
            query_bundle
        )

        sql_query_str = metadata["sql_query"]
        if self._synthesize_response:
            partial_synthesis_prompt = self._response_synthesis_prompt.partial_format(
                sql_query=sql_query_str,
            )
            response_synthesizer = get_response_synthesizer(
                service_context=self._service_context,
                callback_manager=self._service_context.callback_manager,
                text_qa_template=partial_synthesis_prompt,
            )
            response = response_synthesizer.synthesize(
                query=query_bundle.query_str,
                nodes=retrieved_nodes,
            )
            cast(Dict, response.metadata).update(metadata)
            return cast(Response, response)
        else:
            response_str = "\n".join([node.node.text for node in retrieved_nodes])
            return Response(response=response_str, metadata=metadata)

    async def _aquery(self, query_bundle: QueryBundle) -> Response:
        """Answer a query."""
        retrieved_nodes, metadata = await self.sql_retriever.aretrieve_with_metadata(
            query_bundle
        )

        sql_query_str = metadata["sql_query"]
        if self._synthesize_response:
            partial_synthesis_prompt = self._response_synthesis_prompt.partial_format(
                sql_query=sql_query_str,
            )
            response_synthesizer = get_response_synthesizer(
                service_context=self._service_context,
                callback_manager=self._service_context.callback_manager,
                text_qa_template=partial_synthesis_prompt,
            )
            response = await response_synthesizer.asynthesize(
                query=query_bundle.query_str,
                nodes=retrieved_nodes,
            )
            cast(Dict, response.metadata).update(metadata)
            return cast(Response, response)
        else:
            response_str = "\n".join([node.node.text for node in retrieved_nodes])
            return Response(response=response_str, metadata=metadata)
