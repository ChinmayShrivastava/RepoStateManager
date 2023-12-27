class IndexType(enum.Enum):
    """Enumerator for the supported Index types."""

    TIMESCALE_VECTOR = 1
    PGVECTOR_IVFFLAT = 2
    PGVECTOR_HNSW = 3
