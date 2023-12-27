class BaseSelector(PromptMixin):
    def _get_prompt_modules(self) -> PromptMixinType:
        """Get prompt sub-modules."""
        return {}

    def select(
        self, choices: Sequence[MetadataType], query: QueryType
    ) -> SelectorResult:
        metadatas = [_wrap_choice(choice) for choice in choices]
        query_bundle = _wrap_query(query)
        return self._select(choices=metadatas, query=query_bundle)

    async def aselect(
        self, choices: Sequence[MetadataType], query: QueryType
    ) -> SelectorResult:
        metadatas = [_wrap_choice(choice) for choice in choices]
        query_bundle = _wrap_query(query)
        return await self._aselect(choices=metadatas, query=query_bundle)

    @abstractmethod
    def _select(
        self, choices: Sequence[ToolMetadata], query: QueryBundle
    ) -> SelectorResult:
        pass

    @abstractmethod
    async def _aselect(
        self, choices: Sequence[ToolMetadata], query: QueryBundle
    ) -> SelectorResult:
        pass
