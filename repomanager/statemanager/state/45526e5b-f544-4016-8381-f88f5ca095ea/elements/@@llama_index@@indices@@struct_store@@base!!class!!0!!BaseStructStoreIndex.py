class BaseStructStoreIndex(BaseIndex[BST], Generic[BST]):
    """Base Struct Store Index."""

    def __init__(
        self,
        nodes: Optional[Sequence[BaseNode]] = None,
        index_struct: Optional[BST] = None,
        service_context: Optional[ServiceContext] = None,
        schema_extract_prompt: Optional[BasePromptTemplate] = None,
        output_parser: Optional[OUTPUT_PARSER_TYPE] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        self.schema_extract_prompt = (
            schema_extract_prompt or DEFAULT_SCHEMA_EXTRACT_PROMPT
        )
        self.output_parser = output_parser or default_output_parser
        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            service_context=service_context,
            **kwargs,
        )

    def _delete_node(self, node_id: str, **delete_kwargs: Any) -> None:
        """Delete a node."""
        raise NotImplementedError("Delete not implemented for Struct Store Index.")

    @property
    def ref_doc_info(self) -> Dict[str, RefDocInfo]:
        """Retrieve a dict mapping of ingested documents and their nodes+metadata."""
        raise NotImplementedError("Struct Store Index does not support ref_doc_info.")
