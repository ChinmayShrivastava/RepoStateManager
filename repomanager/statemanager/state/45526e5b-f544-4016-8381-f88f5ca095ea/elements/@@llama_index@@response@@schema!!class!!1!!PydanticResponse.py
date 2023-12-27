class PydanticResponse:
    """PydanticResponse object.

    Returned if streaming=False.

    Attributes:
        response: The response text.

    """

    response: Optional[BaseModel]
    source_nodes: List[NodeWithScore] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        """Convert to string representation."""
        return self.response.json() if self.response else "None"

    def __getattr__(self, name: str) -> Any:
        """Get attribute, but prioritize the pydantic  response object."""
        if self.response is not None and name in self.response.dict():
            return getattr(self.response, name)
        else:
            return None

    def get_formatted_sources(self, length: int = 100) -> str:
        """Get formatted sources text."""
        texts = []
        for source_node in self.source_nodes:
            fmt_text_chunk = truncate_text(source_node.node.get_content(), length)
            doc_id = source_node.node.node_id or "None"
            source_text = f"> Source (Doc id: {doc_id}): {fmt_text_chunk}"
            texts.append(source_text)
        return "\n\n".join(texts)

    def get_response(self) -> Response:
        """Get a standard response object."""
        response_txt = self.response.json() if self.response else "None"
        return Response(response_txt, self.source_nodes, self.metadata)
