class DBEmbeddingRow(NamedTuple):
    node_id: str  # FIXME: verify this type hint
    text: str
    metadata: dict
    similarity: float
