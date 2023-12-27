class QueryData:
    """
    Query data with column names following the OpenInference specification.
    """

    id: str = field(
        default_factory=_generate_random_id,
        metadata={OPENINFERENCE_COLUMN_NAME: ":id.id:"},
    )
    timestamp: Optional[str] = field(
        default=None, metadata={OPENINFERENCE_COLUMN_NAME: ":timestamp.iso_8601:"}
    )
    query_text: Optional[str] = field(
        default=None,
        metadata={OPENINFERENCE_COLUMN_NAME: ":feature.text:prompt"},
    )
    query_embedding: Optional[Embedding] = field(
        default=None,
        metadata={OPENINFERENCE_COLUMN_NAME: ":feature.[float].embedding:prompt"},
    )
    response_text: Optional[str] = field(
        default=None, metadata={OPENINFERENCE_COLUMN_NAME: ":prediction.text:response"}
    )
    node_ids: List[str] = field(
        default_factory=list,
        metadata={
            OPENINFERENCE_COLUMN_NAME: ":feature.[str].retrieved_document_ids:prompt"
        },
    )
    scores: List[float] = field(
        default_factory=list,
        metadata={
            OPENINFERENCE_COLUMN_NAME: (
                ":feature.[float].retrieved_document_scores:prompt"
            )
        },
    )
